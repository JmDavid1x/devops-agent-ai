from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.models.db_models import HealthCheckResult, ServiceConfig
from app.models.schemas import (
    HealthCheckResultResponse,
    ServiceConfigCreate,
    ServiceConfigResponse,
    ServiceWithHealth,
)
from app.services.health_checker import health_checker

router = APIRouter(prefix="/api", tags=["services"])


@router.get("/services", response_model=list[ServiceWithHealth])
async def list_services(db: AsyncSession = Depends(get_db)) -> list[ServiceWithHealth]:
    """Return all services with their latest health status."""
    result = await db.execute(
        select(ServiceConfig).options(selectinload(ServiceConfig.health_checks))
    )
    services = result.scalars().all()

    response = []
    for svc in services:
        latest = svc.health_checks[0] if svc.health_checks else None
        response.append(ServiceWithHealth(
            id=svc.id,
            name=svc.name,
            url=svc.url,
            status=latest.status if latest else "unknown",
            last_check=latest.checked_at.isoformat() if latest else None,
            response_time_ms=latest.response_time_ms if latest else None,
            is_active=svc.is_active,
        ))
    return response


@router.post("/services", response_model=ServiceConfigResponse)
async def create_service(data: ServiceConfigCreate, db: AsyncSession = Depends(get_db)) -> ServiceConfigResponse:
    """Register a new service to monitor."""
    existing = await db.execute(
        select(ServiceConfig).where(ServiceConfig.name == data.name)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=409, detail=f"Service '{data.name}' already exists")

    service = ServiceConfig(
        name=data.name,
        url=data.url,
        check_interval_seconds=data.check_interval_seconds,
        timeout_seconds=data.timeout_seconds,
        expected_status_code=data.expected_status_code,
    )
    db.add(service)
    await db.commit()
    await db.refresh(service)
    return ServiceConfigResponse(
        id=service.id,
        name=service.name,
        url=service.url,
        check_interval_seconds=service.check_interval_seconds,
        timeout_seconds=service.timeout_seconds,
        expected_status_code=service.expected_status_code,
        is_active=service.is_active,
        created_at=service.created_at,
        updated_at=service.updated_at,
    )


@router.get("/services/{service_id}")
async def get_service(service_id: str, db: AsyncSession = Depends(get_db)):
    """Get a specific service with its latest health."""
    result = await db.execute(
        select(ServiceConfig).where(ServiceConfig.id == service_id)
    )
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    health_result = await db.execute(
        select(HealthCheckResult)
        .where(HealthCheckResult.service_id == service_id)
        .order_by(HealthCheckResult.checked_at.desc())
        .limit(1)
    )
    latest = health_result.scalar_one_or_none()

    return ServiceWithHealth(
        id=service.id,
        name=service.name,
        url=service.url,
        status=latest.status if latest else "unknown",
        last_check=latest.checked_at.isoformat() if latest else None,
        response_time_ms=latest.response_time_ms if latest else None,
        is_active=service.is_active,
    )


@router.delete("/services/{service_id}")
async def delete_service(service_id: str, db: AsyncSession = Depends(get_db)):
    """Remove a service from monitoring."""
    result = await db.execute(
        select(ServiceConfig).where(ServiceConfig.id == service_id)
    )
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    await db.delete(service)
    await db.commit()
    return {"message": f"Service '{service.name}' deleted"}


@router.post("/services/{service_id}/check", response_model=HealthCheckResultResponse)
async def check_service_now(service_id: str, db: AsyncSession = Depends(get_db)):
    """Trigger an immediate health check for a service."""
    result = await db.execute(
        select(ServiceConfig).where(ServiceConfig.id == service_id)
    )
    service = result.scalar_one_or_none()
    if not service:
        raise HTTPException(status_code=404, detail="Service not found")

    check_result = await health_checker.check(
        url=service.url,
        timeout=service.timeout_seconds,
        expected_status=service.expected_status_code,
    )

    record = HealthCheckResult(
        service_id=service.id,
        status=check_result["status"],
        response_time_ms=check_result["response_time_ms"],
        status_code=check_result["status_code"],
        error_message=check_result["error_message"],
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)

    return HealthCheckResultResponse(
        id=record.id,
        service_id=record.service_id,
        status=record.status,
        response_time_ms=record.response_time_ms,
        status_code=record.status_code,
        error_message=record.error_message,
        checked_at=record.checked_at,
    )


@router.get("/services/{service_id}/history", response_model=list[HealthCheckResultResponse])
async def get_service_history(service_id: str, limit: int = 20, db: AsyncSession = Depends(get_db)):
    """Get health check history for a service."""
    result = await db.execute(
        select(HealthCheckResult)
        .where(HealthCheckResult.service_id == service_id)
        .order_by(HealthCheckResult.checked_at.desc())
        .limit(limit)
    )
    records = result.scalars().all()
    return [
        HealthCheckResultResponse(
            id=r.id,
            service_id=r.service_id,
            status=r.status,
            response_time_ms=r.response_time_ms,
            status_code=r.status_code,
            error_message=r.error_message,
            checked_at=r.checked_at,
        )
        for r in records
    ]
