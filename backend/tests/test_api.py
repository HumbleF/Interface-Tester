from pathlib import Path

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_send_single_request(client: AsyncClient, mock_game_server):
    resp = await client.post("/api/request/send", json={
        "server": {"host": "127.0.0.1", "port": mock_game_server},
        "service": "LuckyTurn",
        "method": "LuckyTurnReward",
        "headers": {"numid": "300231159", "areaid": "5016"},
        "body": {"current_count": 1},
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["status_code"] == 200
    assert data["body"]["code"] == 0


@pytest.mark.asyncio
async def test_send_concurrent_request(client: AsyncClient, mock_game_server):
    resp = await client.post("/api/request/concurrent", json={
        "server": {"host": "127.0.0.1", "port": mock_game_server},
        "service": "LuckyTurn",
        "method": "LuckyTurnReward",
        "user_ids": ["100001", "100002", "100003"],
        "areaid": "5016",
        "body": {"current_count": 1},
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["total"] == 3
    assert len(data["results"]) == 3


@pytest.mark.asyncio
async def test_mock_purchase(client: AsyncClient, mock_purchase_server):
    resp = await client.post("/api/mock/purchase", json={
        "server": {"host": "127.0.0.1", "port": mock_purchase_server},
        "numid": "300231159",
        "areaid": "5016",
        "product_id": 80001,
        "event": 1,
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["success"] is True
    assert data["pre_order_no"] != ""


@pytest.mark.asyncio
async def test_task_cmd(client: AsyncClient, mock_game_server):
    resp = await client.post("/api/mock/task-cmd", json={
        "server": {"host": "127.0.0.1", "port": mock_game_server},
        "numid": "300231159",
        "areaid": "5016",
        "cmd": "finish",
        "task_id": [240],
    })
    assert resp.status_code == 200
    data = resp.json()
    assert data["body"]["code"] == 0


@pytest.mark.asyncio
async def test_config_save_and_load(client: AsyncClient):
    config = {
        "server_host": "192.168.1.100",
        "server_port": 14354,
        "areaid": "5016",
        "user_ids": ["300231159", "300231160"],
    }
    resp = await client.post("/api/config/save", json=config)
    assert resp.status_code == 200

    resp = await client.get("/api/config/load")
    assert resp.status_code == 200
    data = resp.json()
    assert data["server_host"] == "192.168.1.100"
    assert data["user_ids"] == ["300231159", "300231160"]
