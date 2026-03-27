from fastapi import APIRouter, HTTPException

from app.models.schemas import Container
from app.services.docker_service import docker_service

router = APIRouter(prefix="/api/docker", tags=["docker"])


@router.get("/containers", response_model=list[Container])
async def list_containers() -> list[Container]:
    """Return a list of Docker containers."""
    containers = docker_service.list_containers(all=True, include_stats=False)
    return [Container(**c) for c in containers]


@router.get("/containers/{container_id}/stats")
async def get_container_stats(container_id: str) -> dict:
    """Get real-time stats for a Docker container."""
    result = docker_service.get_container_stats(container_id)
    if "error" in result and "not found" in result["error"].lower():
        raise HTTPException(status_code=404, detail=result["error"])
    return result


@router.post("/containers/{container_id}/restart")
async def restart_container(container_id: str) -> dict:
    """Restart a Docker container by ID."""
    result = docker_service.restart_container(container_id)
    if "error" in result and "not found" in result["error"].lower():
        raise HTTPException(status_code=404, detail=result["error"])
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.post("/containers/{container_id}/stop")
async def stop_container(container_id: str) -> dict:
    """Stop a Docker container by ID."""
    result = docker_service.stop_container(container_id)
    if "error" in result and "not found" in result["error"].lower():
        raise HTTPException(status_code=404, detail=result["error"])
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result


@router.post("/containers/{container_id}/start")
async def start_container(container_id: str) -> dict:
    """Start a Docker container by ID."""
    result = docker_service.start_container(container_id)
    if "error" in result and "not found" in result["error"].lower():
        raise HTTPException(status_code=404, detail=result["error"])
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    return result
