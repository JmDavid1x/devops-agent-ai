from datetime import datetime

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    tools_used: list[str] = []


class ServiceConfigCreate(BaseModel):
    name: str
    url: str
    check_interval_seconds: int = 60
    timeout_seconds: int = 10
    expected_status_code: int = 200


class ServiceConfigResponse(BaseModel):
    id: str
    name: str
    url: str
    check_interval_seconds: int
    timeout_seconds: int
    expected_status_code: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class HealthCheckResultResponse(BaseModel):
    id: str
    service_id: str
    status: str
    response_time_ms: float | None = None
    status_code: int | None = None
    error_message: str | None = None
    checked_at: datetime


class ServiceWithHealth(BaseModel):
    id: str
    name: str
    url: str
    status: str = "unknown"
    last_check: str | None = None
    response_time_ms: float | None = None
    is_active: bool = True


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
    state: str | None = None
    ports: list[str] = []
    cpu: str | None = None
    memory: str | None = None
    created: str | None = None


class HealthCheck(BaseModel):
    service_id: str
    status: str
    response_time_ms: float
    timestamp: str


class MessageSchema(BaseModel):
    id: str
    role: str
    content: str
    tools_used: list[str] | None = None
    created_at: datetime


class ConversationSchema(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    messages: list[MessageSchema] = []


class ConversationListItem(BaseModel):
    id: str
    title: str
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
