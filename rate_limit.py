import os

from slowapi import Limiter
from starlette.requests import Request

QUERY_RATE_LIMIT = os.getenv("RATE_LIMIT_QUERY", "10/minute")
HEALTH_RATE_LIMIT = os.getenv("RATE_LIMIT_HEALTH", "60/minute")


def get_client_ip(request: Request) -> str:
    """
    Returns the client IP used as rate limit key.

    Behind the nginx proxy the last X-Forwarded-For entry is the one appended by
    nginx (the real peer); earlier entries can be forged by the client.
    """
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[-1].strip()
    return request.client.host if request.client else "unknown"


limiter = Limiter(key_func=get_client_ip)
