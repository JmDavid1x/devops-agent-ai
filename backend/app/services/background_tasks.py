import asyncio
import logging

from sqlalchemy import select

from app.core.database import async_session
from app.models.db_models import HealthCheckResult, ServiceConfig
from app.services.health_checker import health_checker

logger = logging.getLogger(__name__)


async def run_health_checks():
    """Run health checks for all active services."""
    async with async_session() as session:
        result = await session.execute(
            select(ServiceConfig).where(ServiceConfig.is_active == True)
        )
        services = result.scalars().all()

        for service in services:
            check_result = await health_checker.check(
                url=service.url,
                timeout=service.timeout_seconds,
                expected_status=service.expected_status_code,
            )

            health_record = HealthCheckResult(
                service_id=service.id,
                status=check_result["status"],
                response_time_ms=check_result["response_time_ms"],
                status_code=check_result["status_code"],
                error_message=check_result["error_message"],
            )
            session.add(health_record)

        await session.commit()
        logger.info(f"Health checks completed for {len(services)} services")


async def periodic_health_checks(interval: int = 60):
    """Run health checks periodically."""
    while True:
        try:
            await run_health_checks()
        except Exception as e:
            logger.error(f"Periodic health check error: {e}")
        await asyncio.sleep(interval)
