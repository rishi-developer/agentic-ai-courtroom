from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config.settings import settings
from app.database.connection import create_tables
from app.models import Case
from app.api.case_routes import router as case_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(
    title=settings.APP_NAME,
    description="An Agentic AI-powered courtroom simulation",
    version="1.0.0",
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.include_router(case_router)

@app.get("/")
async def home():
    return {
        "message": f"Welcome to {settings.APP_NAME}"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}