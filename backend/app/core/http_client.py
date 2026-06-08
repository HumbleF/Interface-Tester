import asyncio
import time

import aiohttp

from app.models.request_models import (
    ConcurrentRequest,
    ConcurrentResponse,
    ConcurrentResponseItem,
    SingleRequest,
    SingleResponse,
)


async def send_single(req: SingleRequest) -> SingleResponse:
    url = f"http://{req.server.host}:{req.server.port}/{req.service}/{req.method}"
    headers = {"Content-Type": "application/json"}
    headers.update(req.headers)

    start = time.monotonic()
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=req.body, headers=headers) as resp:
                body = await resp.json()
                elapsed_ms = (time.monotonic() - start) * 1000
                return SingleResponse(
                    status_code=resp.status,
                    body=body,
                    elapsed_ms=round(elapsed_ms, 2),
                )
    except Exception as e:
        elapsed_ms = (time.monotonic() - start) * 1000
        return SingleResponse(
            status_code=0,
            body={"error": str(e)},
            elapsed_ms=round(elapsed_ms, 2),
        )


async def _send_one(
    session: aiohttp.ClientSession,
    url: str,
    numid: str,
    areaid: str,
    body: dict,
) -> ConcurrentResponseItem:
    headers = {
        "Content-Type": "application/json",
        "numid": numid,
        "areaid": areaid,
    }
    start = time.monotonic()
    try:
        async with session.post(url, json=body, headers=headers) as resp:
            resp_body = await resp.json()
            elapsed_ms = (time.monotonic() - start) * 1000
            return ConcurrentResponseItem(
                numid=numid,
                status_code=resp.status,
                body=resp_body,
                elapsed_ms=round(elapsed_ms, 2),
            )
    except Exception as e:
        elapsed_ms = (time.monotonic() - start) * 1000
        return ConcurrentResponseItem(
            numid=numid,
            status_code=0,
            body={},
            elapsed_ms=round(elapsed_ms, 2),
            error=str(e),
        )


async def send_concurrent(req: ConcurrentRequest) -> ConcurrentResponse:
    url = f"http://{req.server.host}:{req.server.port}/{req.service}/{req.method}"
    start = time.monotonic()
    async with aiohttp.ClientSession() as session:
        tasks = [
            _send_one(session, url, numid, req.areaid, req.body)
            for numid in req.user_ids
        ]
        results = await asyncio.gather(*tasks)
    total_elapsed_ms = (time.monotonic() - start) * 1000
    return ConcurrentResponse(
        total=len(results),
        results=list(results),
        total_elapsed_ms=round(total_elapsed_ms, 2),
    )
