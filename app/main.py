from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="Lab 3 FastAPI CRUD")

app.include_router(api_router)