import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)

# Registry of tool implementations
TOOL_REGISTRY: dict = {}


def register_tool(name: str):
    """Decorator to register a tool implementation."""
    def decorator(func):
        TOOL_REGISTRY[name] = func
        return func
    return decorator


async def execute_tool(name: str, arguments: dict) -> dict:
    """Execute a tool by name with the given arguments."""
    if name not in TOOL_REGISTRY:
        return {"error": f"Unknown tool: {name}"}

    try:
        result = await TOOL_REGISTRY[name](**arguments)
        return result
    except Exception as e:
        logger.error(f"Tool {name} failed: {e}")
        return {"error": f"Tool execution failed: {str(e)}"}


@register_tool("analyze_logs")
async def analyze_logs(service_name: str, time_range: str = "1h", severity: str = "warning") -> dict:
    """Analyze logs for a service. Returns mock data for now."""
    now = datetime.now(timezone.utc).isoformat()
    return {
        "service": service_name,
        "time_range": time_range,
        "severity_filter": severity,
        "analyzed_at": now,
        "total_entries": 1547,
        "summary": {
            "errors": 12,
            "warnings": 45,
            "info": 1490,
        },
        "top_errors": [
            {"message": "Connection timeout to database", "count": 5, "last_seen": now},
            {"message": "Failed to parse request body", "count": 4, "last_seen": now},
            {"message": "Memory usage exceeded threshold", "count": 3, "last_seen": now},
        ],
        "recommendation": f"Service '{service_name}' shows database connection issues. Consider checking the database connection pool settings.",
    }


@register_tool("check_service_health")
async def check_service_health(service_name: str, url: str | None = None) -> dict:
    """Check health of a service using real HTTP requests."""
    from app.services.health_checker import health_checker

    target_url = url or f"http://{service_name}:8080/health"
    result = await health_checker.check(url=target_url)
    result["service"] = service_name
    result["url"] = target_url
    result["checked_at"] = datetime.now(timezone.utc).isoformat()
    return result


@register_tool("list_containers")
async def list_containers(status_filter: str = "all") -> dict:
    """List Docker containers using the real Docker daemon."""
    from app.services.docker_service import docker_service

    show_all = status_filter == "all"
    containers = docker_service.list_containers(all=show_all, include_stats=True)

    if status_filter != "all":
        containers = [c for c in containers if c["status"] == status_filter]

    return {
        "containers": containers,
        "total": len(containers),
        "filter": status_filter,
        "docker_available": docker_service.is_available,
    }


@register_tool("restart_container")
async def restart_container(container_id: str, timeout: int = 10) -> dict:
    """Restart a Docker container using the real Docker daemon."""
    from app.services.docker_service import docker_service

    result = docker_service.restart_container(container_id, timeout=timeout)
    result["action"] = "restart"
    result["restarted_at"] = datetime.now(timezone.utc).isoformat()
    return result


@register_tool("deploy_service")
async def deploy_service(service_name: str, image: str, environment: str = "development", strategy: str = "rolling") -> dict:
    """Deploy a service. Returns mock data for now."""
    return {
        "service": service_name,
        "image": image,
        "environment": environment,
        "strategy": strategy,
        "status": "deployed",
        "deployment_id": "deploy-20240101-001",
        "started_at": datetime.now(timezone.utc).isoformat(),
        "message": f"Service '{service_name}' deployed to {environment} using {strategy} strategy.",
    }
