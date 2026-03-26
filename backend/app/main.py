import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.chat import router as chat_router
from app.api.conversations import router as conversations_router
from app.api.docker_routes import router as docker_router
from app.api.services import router as services_router
from app.core.database import init_db

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    await init_db()
    yield


app = FastAPI(title="DevOps AI Agent API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(conversations_router)
app.include_router(services_router)
app.include_router(docker_router)


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy"}


@app.get("/")
async def root() -> dict:
    return {"message": "DevOps AI Agent API", "version": "1.0.0"}
