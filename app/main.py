from fastapi import FastAPI
from app.routers import tasks
from app.database import engine, Base

# Crée les tables si elles n'existent pas encore
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DevOps Showcase API",
    description="API de démonstration - projet portfolio DevOps",
    version="1.0.0",
)

app.include_router(tasks.router, prefix="/tasks", tags=["tasks"])


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "version": "1.0.0"}