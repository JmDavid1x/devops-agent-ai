import logging
from datetime import datetime, timezone

import httpx

logger = logging.getLogger(__name__)


class HealthChecker:
    async def check(self, url: str, timeout: int = 10, expected_status: int = 200) -> dict:
        try:
            async with httpx.AsyncClient() as client:
                start = datetime.now(timezone.utc)
                response = await client.get(url, timeout=timeout, follow_redirects=True)
                elapsed_ms = (datetime.now(timezone.utc) - start).total_seconds() * 1000

                if response.status_code == expected_status:
                    status = "degraded" if elapsed_ms > 5000 else "healthy"
                else:
                    status = "degraded"

                return {
                    "status": status,
                    "response_time_ms": round(elapsed_ms, 2),
                    "status_code": response.status_code,
                    "error_message": None,
                }
        except httpx.TimeoutException:
            return {
                "status": "down",
                "response_time_ms": None,
                "status_code": None,
                "error_message": "Connection timeout",
            }
        except httpx.ConnectError:
            return {
                "status": "down",
                "response_time_ms": None,
                "status_code": None,
                "error_message": "Connection refused",
            }
        except Exception as e:
            logger.error(f"Health check failed for {url}: {e}")
            return {
                "status": "down",
                "response_time_ms": None,
                "status_code": None,
                "error_message": str(e),
            }


health_checker = HealthChecker()
