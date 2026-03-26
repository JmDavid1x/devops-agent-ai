"""Agent tool definitions for the DevOps AI Agent.

Each tool follows a common schema compatible with both Claude and OpenAI
function-calling formats: name, description, and a JSON Schema parameters object.
"""

TOOL_ANALYZE_LOGS: dict = {
    "name": "analyze_logs",
    "description": (
        "Analyze application logs for errors, warnings, and anomalies. "
        "Provide a summary of issues found and suggested actions."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "service_name": {
                "type": "string",
                "description": "Name of the service whose logs to analyze.",
            },
            "time_range": {
                "type": "string",
                "description": "Time range for log analysis, e.g. '1h', '24h', '7d'.",
                "default": "1h",
            },
            "severity": {
                "type": "string",
                "enum": ["error", "warning", "info", "debug"],
                "description": "Minimum severity level to include.",
                "default": "warning",
            },
        },
        "required": ["service_name"],
    },
}

TOOL_CHECK_SERVICE_HEALTH: dict = {
    "name": "check_service_health",
    "description": (
        "Check the health status of a service by sending a request "
        "to its health endpoint and reporting response time and status."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "service_name": {
                "type": "string",
                "description": "Name of the service to check.",
            },
            "url": {
                "type": "string",
                "description": "Optional URL to use instead of the registered service URL.",
            },
        },
        "required": ["service_name"],
    },
}

TOOL_LIST_CONTAINERS: dict = {
    "name": "list_containers",
    "description": (
        "List Docker containers with their status, image, and port mappings. "
        "Can filter by status (running, stopped, all)."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "status_filter": {
                "type": "string",
                "enum": ["running", "stopped", "all"],
                "description": "Filter containers by status.",
                "default": "all",
            },
        },
        "required": [],
    },
}

TOOL_RESTART_CONTAINER: dict = {
    "name": "restart_container",
    "description": (
        "Restart a Docker container by its ID or name. "
        "Returns the new status after the restart."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "container_id": {
                "type": "string",
                "description": "The container ID or name to restart.",
            },
            "timeout": {
                "type": "integer",
                "description": "Seconds to wait before killing the container.",
                "default": 10,
            },
        },
        "required": ["container_id"],
    },
}

TOOL_DEPLOY_SERVICE: dict = {
    "name": "deploy_service",
    "description": (
        "Deploy or update a service. Supports rolling updates and rollbacks. "
        "Returns deployment status and details."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "service_name": {
                "type": "string",
                "description": "Name of the service to deploy.",
            },
            "image": {
                "type": "string",
                "description": "Docker image to deploy, e.g. 'myapp:latest'.",
            },
            "environment": {
                "type": "string",
                "enum": ["development", "staging", "production"],
                "description": "Target deployment environment.",
                "default": "development",
            },
            "strategy": {
                "type": "string",
                "enum": ["rolling", "recreate", "blue-green"],
                "description": "Deployment strategy to use.",
                "default": "rolling",
            },
        },
        "required": ["service_name", "image"],
    },
}

ALL_TOOLS: list[dict] = [
    TOOL_ANALYZE_LOGS,
    TOOL_CHECK_SERVICE_HEALTH,
    TOOL_LIST_CONTAINERS,
    TOOL_RESTART_CONTAINER,
    TOOL_DEPLOY_SERVICE,
]
