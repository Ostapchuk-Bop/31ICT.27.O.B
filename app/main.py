from fastapi import FastAPI
from app.api.router import api_router
from app.db.base import Base
from app.db.session import engine
from app.monitoring import setup_metrics
from app import models  # Ensure all models are registered

app = FastAPI(title="Lab 4 FastAPI PostgreSQL CRUD")

# @app.on_event("startup")
# async def create_tables():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

app.include_router(api_router)
setup_metrics(app)
