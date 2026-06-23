"""FastAPI application entry point."""

from fastapi import FastAPI

from app.routes import router

app = FastAPI(
    title="Bookmarks Service",
    description="A small in-memory bookmarks REST API used for testing.",
    version="0.1.0",
)

app.include_router(router)
