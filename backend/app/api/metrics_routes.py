from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.security import verify_api_key
from app.models.db_models import Conversation, Message, User, ServiceConfig, HealthCheckResult

router = APIRouter(prefix="/api/metrics", tags=["metrics"], dependencies=[Depends(verify_api_key)])


@router.get("/summary")
async def get_metrics_summary(db: AsyncSession = Depends(get_db)):
    """Return aggregated metrics for the frontend monitoring page."""
    # Count users
    user_count = await db.execute(select(func.count(User.id)))
    total_users = user_count.scalar() or 0

    # Count conversations
    conv_count = await db.execute(select(func.count(Conversation.id)))
    total_conversations = conv_count.scalar() or 0

    # Count messages
    msg_count = await db.execute(select(func.count(Message.id)))
    total_messages = msg_count.scalar() or 0

    # Count services
    svc_count = await db.execute(select(func.count(ServiceConfig.id)))
    total_services = svc_count.scalar() or 0

    # Latest health checks per service
    services_result = await db.execute(select(ServiceConfig).where(ServiceConfig.is_active == True))
    services = services_result.scalars().all()

    service_health = []
    for svc in services:
        latest_result = await db.execute(
            select(HealthCheckResult)
            .where(HealthCheckResult.service_id == svc.id)
            .order_by(HealthCheckResult.checked_at.desc())
            .limit(1)
        )
        latest = latest_result.scalar_one_or_none()
        service_health.append({
            "name": svc.name,
            "status": latest.status if latest else "unknown",
            "response_time_ms": latest.response_time_ms if latest else None,
            "last_check": latest.checked_at.isoformat() if latest else None,
        })

    # Count health checks
    health_count = await db.execute(select(func.count(HealthCheckResult.id)))
    total_health_checks = health_count.scalar() or 0

    return {
        "users": total_users,
        "conversations": total_conversations,
        "messages": total_messages,
        "services": total_services,
        "health_checks_performed": total_health_checks,
        "service_health": service_health,
    }
