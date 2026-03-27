import asyncio
import logging

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.conversations import router as conversations_router
from app.api.docker_routes import router as docker_router
from app.api.metrics_routes import router as metrics_router
from app.api.services import router as services_router
from app.core.config import settings
from app.core.database import init_db
from app.core.security import SecurityHeadersMiddleware
from app.services.background_tasks import periodic_health_checks

logging.basicConfig(level=logging.INFO)

limiter = Limiter(key_func=get_remote_address)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events."""
    await init_db()
    health_task = asyncio.create_task(periodic_health_checks(interval=60))
    yield
    health_task.cancel()
    try:
        await health_task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="DevOps AI Agent API", version="1.0.0", lifespan=lifespan)

# Prometheus instrumentation
Instrumentator().instrument(app).expose(app, endpoint="/metrics")

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Security headers
app.add_middleware(SecurityHeadersMiddleware)

# CORS
allowed_origins = [o.strip() for o in settings.allowed_origins.split(",") if o.strip()]
if settings.debug and not allowed_origins:
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(conversations_router)
app.include_router(services_router)
app.include_router(docker_router)
app.include_router(metrics_router)


@app.get("/health")
async def health_check() -> dict:
    return {"status": "healthy"}


@app.get("/")
async def root() -> dict:
    return {"message": "DevOps AI Agent API", "version": "1.0.0"}
