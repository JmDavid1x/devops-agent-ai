from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tools_used: list[str] = []


class Service(BaseModel):
    id: str
    name: str
    url: str
    status: str
    last_check: str | None = None


class Container(BaseModel):
    id: str
    name: str
    image: str
    status: str
    ports: list[str] = []


class HealthCheck(BaseModel):
    service_id: str
    status: str
    response_time_ms: float
    timestamp: str
