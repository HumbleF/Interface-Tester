import asyncio
from aiohttp import web
import pytest

from app.core.http_client import send_single, send_concurrent
from app.models.request_models import (
    ConcurrentRequest,
    SingleRequest,
    TargetServer,
)


@pytest.fixture
async def mock_server(unused_tcp_port):
    """Minimal HTTP server that echoes request info."""
    async def handler(request: web.Request):
        body = await request.json() if request.content_length else {}
        return web.json_response({
            "code": 0,
            "data": {
                "numid": request.headers.get("numid", ""),
                "path": request.path,
                "body": body,
            },
        })

    app = web.Application()
    app.router.add_post("/{service}/{method}", handler)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "127.0.0.1", unused_tcp_port)
    await site.start()
    yield unused_tcp_port
    await runner.cleanup()


@pytest.mark.asyncio
async def test_send_single(mock_server):
    req = SingleRequest(
        server=TargetServer(host="127.0.0.1", port=mock_server),
        service="LuckyTurn",
        method="LuckyTurnReward",
        headers={"numid": "300231159", "areaid": "5016"},
        body={"current_count": 1},
    )
    resp = await send_single(req)
    assert resp.status_code == 200
    assert resp.body["code"] == 0
    assert resp.body["data"]["numid"] == "300231159"
    assert resp.body["data"]["path"] == "/LuckyTurn/LuckyTurnReward"


@pytest.mark.asyncio
async def test_send_concurrent(mock_server):
    req = ConcurrentRequest(
        server=TargetServer(host="127.0.0.1", port=mock_server),
        service="LuckyTurn",
        method="LuckyTurnReward",
        user_ids=["100001", "100002", "100003"],
        areaid="5016",
        body={"current_count": 1},
    )
    resp = await send_concurrent(req)
    assert resp.total == 3
    assert len(resp.results) == 3
    returned_ids = {r.numid for r in resp.results}
    assert returned_ids == {"100001", "100002", "100003"}
    for r in resp.results:
        assert r.status_code == 200
        assert r.body["code"] == 0


@pytest.mark.asyncio
async def test_concurrent_single_failure_does_not_affect_others(mock_server, unused_tcp_port):
    """A single request failure should not block others."""
    bad_req = ConcurrentRequest(
        server=TargetServer(host="127.0.0.1", port=unused_tcp_port),
        service="LuckyTurn",
        method="LuckyTurnReward",
        user_ids=["100001", "100002"],
        areaid="5016",
        body={"current_count": 1},
    )
    resp = await send_concurrent(bad_req)
    assert resp.total == 2
    assert len(resp.results) == 2
    for r in resp.results:
        assert r.error != "" or r.status_code > 0
