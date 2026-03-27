from prometheus_client import Counter, Gauge, Histogram

# Chat metrics
CHAT_REQUESTS = Counter(
    "chat_requests_total",
    "Total chat requests processed",
    ["status"],
)

# Tool execution metrics
TOOL_EXECUTIONS = Counter(
    "tool_executions_total",
    "Total tool executions",
    ["tool_name", "status"],
)

# AI provider latency
AI_LATENCY = Histogram(
    "ai_provider_latency_seconds",
    "AI provider response time in seconds",
    ["provider"],
    buckets=[0.5, 1.0, 2.5, 5.0, 10.0, 30.0, 60.0],
)

# Service health gauge
SERVICE_HEALTH = Gauge(
    "service_health_status",
    "Service health status (1=healthy, 0.5=degraded, 0=down)",
    ["service_name"],
)

# Active users gauge
ACTIVE_USERS = Gauge(
    "active_users",
    "Number of registered users",
)
