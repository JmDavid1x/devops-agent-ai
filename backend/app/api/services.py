from fastapi import APIRouter

from app.models.schemas import HealthCheck, Service

router = APIRouter(prefix="/api", tags=["services"])

MOCK_SERVICES: list[Service] = [
    Service(
        id="svc-1",
        name="api-gateway",
        url="http://localhost:8080",
        status="healthy",
        last_check="2025-01-01T00:00:00Z",
    ),
    Service(
        id="svc-2",
        name="auth-service",
        url="http://localhost:8081",
        status="healthy",
        last_check="2025-01-01T00:00:00Z",
    ),
    Service(
        id="svc-3",
        name="payment-service",
        url="http://localhost:8082",
        status="degraded",
        last_check="2025-01-01T00:00:00Z",
    ),
]


@router.get("/services", response_model=list[Service])
async def list_services() -> list[Service]:
    """Return a list of registered services with their health status."""
    return MOCK_SERVICES


@router.get("/services/{service_id}/health", response_model=HealthCheck)
async def get_service_health(service_id: str) -> HealthCheck:
    """Return a health check result for a specific service."""
    return HealthCheck(
        service_id=service_id,
        status="healthy",
        response_time_ms=42.5,
        timestamp="2025-01-01T00:00:00Z",
    )
