from fastapi import FastAPI
import os

app = FastAPI()

@app.get("/")
def read_root():
    return {
        "status": "Running",
        "container": "FastAPI",
        "database_url": os.getenv("DATABASE_URL")
    }

@app.get("/health")
def health_check():
    return {"status": "ok"}