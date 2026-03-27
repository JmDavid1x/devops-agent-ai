from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "DevOps AI Agent"
    debug: bool = False
    api_version: str = "v1"
    claude_api_key: str = ""
    openai_api_key: str = ""
    ai_provider: str = "claude"
    database_url: str = "postgresql://postgres:postgres@localhost:5432/devops_agent"
    redis_url: str = "redis://localhost:6379/0"

    # Security
    api_key: str = ""
    allowed_origins: str = "http://localhost:3000"
    rate_limit: str = "60/minute"
    rate_limit_chat: str = "20/minute"

    # JWT (for Phase E)
    jwt_secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60

    model_config = {"env_file": ".env"}


settings = Settings()
