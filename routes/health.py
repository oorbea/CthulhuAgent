from fastapi import APIRouter
from starlette.requests import Request

from rate_limit import HEALTH_RATE_LIMIT, limiter


router = APIRouter(prefix="/api/health", tags=["health"])

@router.get("/")
@limiter.limit(HEALTH_RATE_LIMIT)
def health_check(request: Request):
    return {"status": "ok"}