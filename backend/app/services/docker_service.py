import logging
from typing import Any

logger = logging.getLogger(__name__)

try:
    import docker
    from docker.errors import DockerException, NotFound, APIError
    DOCKER_AVAILABLE = True
except ImportError:
    DOCKER_AVAILABLE = False

MOCK_CONTAINERS = [
    {"id": "abc123def456", "name": "web-api", "image": "devops-agent/api:latest", "status": "running", "state": "running", "ports": ["8080:8080"], "cpu": "2.3%", "memory": "256MB", "created": "2024-01-01T00:00:00Z"},
    {"id": "def456ghi789", "name": "postgres-db", "image": "postgres:16", "status": "running", "state": "running", "ports": ["5432:5432"], "cpu": "1.1%", "memory": "128MB", "created": "2024-01-01T00:00:00Z"},
    {"id": "ghi789jkl012", "name": "redis-cache", "image": "redis:7-alpine", "status": "exited", "state": "exited", "ports": [], "cpu": "0%", "memory": "0MB", "created": "2024-01-01T00:00:00Z"},
]


class DockerService:
    def __init__(self):
        self._client = None
        self._available = False
        if DOCKER_AVAILABLE:
            try:
                self._client = docker.from_env()
                self._client.ping()
                self._available = True
                logger.info("Docker daemon connected successfully")
            except Exception as e:
                logger.warning(f"Docker daemon not available: {e}. Using mock data.")
                self._available = False

    @property
    def is_available(self) -> bool:
        return self._available

    def _parse_ports(self, ports: dict | None) -> list[str]:
        if not ports:
            return []
        result = []
        for container_port, host_bindings in ports.items():
            if host_bindings:
                for binding in host_bindings:
                    host_port = binding.get("HostPort", "")
                    if host_port:
                        result.append(f"{host_port}:{container_port}")
            else:
                result.append(container_port)
        return result

    def _calculate_cpu_percent(self, stats: dict) -> str:
        try:
            cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - stats["precpu_stats"]["cpu_usage"]["total_usage"]
            system_delta = stats["cpu_stats"]["system_cpu_usage"] - stats["precpu_stats"]["system_cpu_usage"]
            num_cpus = stats["cpu_stats"].get("online_cpus", 1)
            if system_delta > 0:
                percent = (cpu_delta / system_delta) * num_cpus * 100.0
                return f"{percent:.1f}%"
        except (KeyError, ZeroDivisionError, TypeError):
            pass
        return "0.0%"

    def _calculate_memory(self, stats: dict) -> str:
        try:
            usage = stats["memory_stats"]["usage"]
            if usage > 1073741824:
                return f"{usage / 1073741824:.1f}GB"
            return f"{usage / 1048576:.0f}MB"
        except (KeyError, TypeError):
            return "0MB"

    def _container_to_dict(self, container: Any, include_stats: bool = False) -> dict:
        ports = self._parse_ports(container.ports)
        image_tags = container.image.tags if container.image.tags else [container.attrs.get("Config", {}).get("Image", "unknown")]
        result = {
            "id": container.short_id,
            "name": container.name,
            "image": image_tags[0] if image_tags else "unknown",
            "status": container.status,
            "state": container.status,
            "ports": ports,
            "created": container.attrs.get("Created", ""),
        }
        if include_stats and container.status == "running":
            try:
                stats = container.stats(stream=False)
                result["cpu"] = self._calculate_cpu_percent(stats)
                result["memory"] = self._calculate_memory(stats)
            except Exception:
                result["cpu"] = "N/A"
                result["memory"] = "N/A"
        else:
            result["cpu"] = "0%" if container.status != "running" else "N/A"
            result["memory"] = "0MB" if container.status != "running" else "N/A"
        return result

    def list_containers(self, all: bool = True, include_stats: bool = False) -> list[dict]:
        if not self._available:
            return MOCK_CONTAINERS
        try:
            containers = self._client.containers.list(all=all)
            return [self._container_to_dict(c, include_stats=include_stats) for c in containers]
        except Exception as e:
            logger.error(f"Failed to list containers: {e}")
            return MOCK_CONTAINERS

    def get_container(self, container_id: str) -> dict | None:
        if not self._available:
            return next((c for c in MOCK_CONTAINERS if c["id"].startswith(container_id)), None)
        try:
            container = self._client.containers.get(container_id)
            return self._container_to_dict(container, include_stats=True)
        except NotFound:
            return None
        except Exception as e:
            logger.error(f"Failed to get container {container_id}: {e}")
            return None

    def restart_container(self, container_id: str, timeout: int = 10) -> dict:
        if not self._available:
            return {"container_id": container_id, "status": "restarted", "message": f"Container {container_id} restarted (mock)"}
        try:
            container = self._client.containers.get(container_id)
            container.restart(timeout=timeout)
            container.reload()
            return {"container_id": container.short_id, "name": container.name, "status": container.status, "message": f"Container {container.name} restarted successfully"}
        except NotFound:
            return {"error": f"Container {container_id} not found"}
        except APIError as e:
            return {"error": f"Failed to restart: {str(e)}"}

    def stop_container(self, container_id: str) -> dict:
        if not self._available:
            return {"container_id": container_id, "status": "stopped", "message": f"Container {container_id} stopped (mock)"}
        try:
            container = self._client.containers.get(container_id)
            container.stop()
            container.reload()
            return {"container_id": container.short_id, "name": container.name, "status": container.status, "message": f"Container {container.name} stopped successfully"}
        except NotFound:
            return {"error": f"Container {container_id} not found"}
        except APIError as e:
            return {"error": f"Failed to stop: {str(e)}"}

    def start_container(self, container_id: str) -> dict:
        if not self._available:
            return {"container_id": container_id, "status": "running", "message": f"Container {container_id} started (mock)"}
        try:
            container = self._client.containers.get(container_id)
            container.start()
            container.reload()
            return {"container_id": container.short_id, "name": container.name, "status": container.status, "message": f"Container {container.name} started successfully"}
        except NotFound:
            return {"error": f"Container {container_id} not found"}
        except APIError as e:
            return {"error": f"Failed to start: {str(e)}"}

    def get_container_stats(self, container_id: str) -> dict:
        if not self._available:
            return {"container_id": container_id, "cpu": "2.3%", "memory": "256MB", "message": "Mock stats"}
        try:
            container = self._client.containers.get(container_id)
            if container.status != "running":
                return {"container_id": container.short_id, "name": container.name, "error": "Container is not running"}
            stats = container.stats(stream=False)
            return {
                "container_id": container.short_id,
                "name": container.name,
                "cpu": self._calculate_cpu_percent(stats),
                "memory": self._calculate_memory(stats),
                "network_rx": self._format_bytes(stats.get("networks", {}).get("eth0", {}).get("rx_bytes", 0)),
                "network_tx": self._format_bytes(stats.get("networks", {}).get("eth0", {}).get("tx_bytes", 0)),
            }
        except NotFound:
            return {"error": f"Container {container_id} not found"}
        except Exception as e:
            return {"error": f"Failed to get stats: {str(e)}"}

    def _format_bytes(self, bytes_val: int) -> str:
        if bytes_val > 1073741824:
            return f"{bytes_val / 1073741824:.1f}GB"
        if bytes_val > 1048576:
            return f"{bytes_val / 1048576:.1f}MB"
        if bytes_val > 1024:
            return f"{bytes_val / 1024:.1f}KB"
        return f"{bytes_val}B"


# Singleton instance
docker_service = DockerService()
