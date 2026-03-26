from fastapi import APIRouter

from app.models.schemas import Container

router = APIRouter(prefix="/api/docker", tags=["docker"])

MOCK_CONTAINERS: list[Container] = [
    Container(
        id="abc123",
        name="nginx-proxy",
        image="nginx:latest",
        status="running",
        ports=["80:80", "443:443"],
    ),
    Container(
        id="def456",
        name="postgres-db",
        image="postgres:16",
        status="running",
        ports=["5432:5432"],
    ),
    Container(
        id="ghi789",
        name="redis-cache",
        image="redis:7-alpine",
        status="exited",
        ports=[],
    ),
]


@router.get("/containers", response_model=list[Container])
async def list_containers() -> list[Container]:
    """Return a list of Docker containers."""
    return MOCK_CONTAINERS


@router.post("/containers/{container_id}/restart")
async def restart_container(container_id: str) -> dict:
    """Restart a Docker container by ID."""
    return {
        "container_id": container_id,
        "status": "restarting",
        "message": f"Container {container_id} is being restarted.",
    }
