from fastapi import APIRouter
from app.api.endpoints import users, posts, categories, comments, tags, profiles

api_router = APIRouter()

# Додаємо маршрути для всіх моделей
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(comments.router, prefix="/comments", tags=["comments"])
api_router.include_router(tags.router, prefix="/tags", tags=["tags"])
api_router.include_router(profiles.router, prefix="/profiles", tags=["profiles"])