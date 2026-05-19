from time import perf_counter

from fastapi import FastAPI, Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from sqlalchemy import func, select
from sqlalchemy.exc import SQLAlchemyError

from app.db.session import AsyncSessionLocal
from app.models.post import Post


REQUEST_COUNT = Counter(
    "fastapi_http_requests_total",
    "Total HTTP requests handled by the FastAPI application.",
    ["method", "path", "status_code"],
)

REQUEST_LATENCY = Histogram(
    "fastapi_http_request_duration_seconds",
    "HTTP request latency in seconds.",
    ["method", "path"],
)

ACTIVE_REQUESTS = Gauge(
    "fastapi_http_requests_in_progress",
    "HTTP requests currently being processed by the FastAPI application.",
)

POSTS_TOTAL = Gauge(
    "fastapi_posts_total",
    "Total number of posts in the application database.",
)

PUBLISHED_POSTS_TOTAL = Gauge(
    "fastapi_published_posts_total",
    "Total number of published posts in the application database.",
)


async def update_custom_metrics() -> None:
    async with AsyncSessionLocal() as session:
        posts_total = await session.scalar(select(func.count(Post.id)))
        published_posts_total = await session.scalar(
            select(func.count(Post.id)).where(Post.published.is_(True))
        )

    POSTS_TOTAL.set(posts_total or 0)
    PUBLISHED_POSTS_TOTAL.set(published_posts_total or 0)


def setup_metrics(app: FastAPI) -> None:
    @app.middleware("http")
    async def prometheus_metrics_middleware(request: Request, call_next):
        ACTIVE_REQUESTS.inc()
        start_time = perf_counter()
        response = None

        try:
            response = await call_next(request)
            return response
        finally:
            duration = perf_counter() - start_time
            route = request.scope.get("route")
            path = getattr(route, "path", request.url.path)
            method = request.method
            status_code = str(response.status_code if response else 500)

            ACTIVE_REQUESTS.dec()
            REQUEST_COUNT.labels(method, path, status_code).inc()
            REQUEST_LATENCY.labels(method, path).observe(duration)

    @app.get("/metrics", include_in_schema=False)
    async def metrics():
        try:
            await update_custom_metrics()
        except SQLAlchemyError:
            pass

        return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
