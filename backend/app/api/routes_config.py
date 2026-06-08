import json

import aiohttp
from fastapi import APIRouter
from pydantic import BaseModel

from app.config import settings

router = APIRouter(prefix="/api/config", tags=["config"])

CONFIG_FILE = "user_config.json"


class UserConfig(BaseModel):
    server_host: str = "121.36.244.219"
    server_port: int = 14354
    areaid: str = "5016"
    user_ids: list[str] = []


@router.get("/load", response_model=UserConfig)
async def load_config():
    config_path = settings.config_dir / CONFIG_FILE
    if not config_path.exists():
        return UserConfig()
    data = json.loads(config_path.read_text(encoding="utf-8"))
    return UserConfig(**data)


@router.post("/save")
async def save_config(config: UserConfig):
    config_path = settings.config_dir / CONFIG_FILE
    config_path.write_text(config.model_dump_json(indent=2), encoding="utf-8")
    return {"saved": True}


class HealthCheckRequest(BaseModel):
    host: str
    port: int


@router.post("/health-check")
async def health_check(req: HealthCheckRequest):
    url = f"http://{req.host}:{req.port}/Health/Ping"
    try:
        timeout = aiohttp.ClientTimeout(total=3)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json={}) as resp:
                return {"reachable": True, "detail": f"HTTP {resp.status}"}
    except aiohttp.ClientConnectorError:
        return {"reachable": False, "detail": "连接被拒绝，服务端未启动或地址不正确"}
    except TimeoutError:
        return {"reachable": False, "detail": "连接超时（3秒），服务端不可达"}
    except Exception as e:
        return {"reachable": False, "detail": str(e)}
