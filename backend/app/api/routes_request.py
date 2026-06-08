from fastapi import APIRouter

from app.core.http_client import send_concurrent, send_single
from app.models.request_models import (
    ConcurrentRequest,
    ConcurrentResponse,
    SingleRequest,
    SingleResponse,
)

router = APIRouter(prefix="/api/request", tags=["request"])


@router.post("/send", response_model=SingleResponse)
async def send_request(req: SingleRequest):
    return await send_single(req)


@router.post("/concurrent", response_model=ConcurrentResponse)
async def send_concurrent_request(req: ConcurrentRequest):
    return await send_concurrent(req)
