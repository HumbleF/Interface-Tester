import aiohttp
from fastapi import APIRouter

from app.core.http_client import send_single
from app.models.request_models import (
    MockPurchaseRequest,
    MockPurchaseResponse,
    SingleRequest,
    SingleResponse,
    TaskCmdRequest,
)

router = APIRouter(prefix="/api/mock", tags=["mock"])


@router.post("/purchase", response_model=MockPurchaseResponse)
async def mock_purchase(req: MockPurchaseRequest):
    base_url = f"http://{req.server.host}:{req.server.port}"
    headers = {
        "Content-Type": "application/json",
        "numid": req.numid,
        "areaid": req.areaid,
    }

    async with aiohttp.ClientSession() as session:
        create_body = {
            "product_id": req.product_id,
            "mock": True,
            "event": req.event,
        }
        try:
            async with session.post(
                f"{base_url}/Product/RechargeCreate",
                json=create_body,
                headers=headers,
            ) as resp:
                create_data = await resp.json()
        except Exception as e:
            return MockPurchaseResponse(success=False, error=f"RechargeCreate failed: {e}")

        if create_data.get("code") != 0:
            return MockPurchaseResponse(
                success=False,
                create_response=create_data,
                error=f"RechargeCreate returned code={create_data.get('code')}",
            )

        pre_order_no = create_data.get("data", {}).get("pre_order_no", "")
        if not pre_order_no:
            return MockPurchaseResponse(
                success=False,
                create_response=create_data,
                error="No pre_order_no in RechargeCreate response",
            )

        delivery_body = {"pre_order_no": pre_order_no}
        try:
            async with session.post(
                f"{base_url}/Product/RechargeDelivery",
                json=delivery_body,
                headers=headers,
            ) as resp:
                delivery_data = await resp.json()
        except Exception as e:
            return MockPurchaseResponse(
                success=False,
                create_response=create_data,
                pre_order_no=pre_order_no,
                error=f"RechargeDelivery failed: {e}",
            )

        success = delivery_data.get("code") == 0
        return MockPurchaseResponse(
            success=success,
            create_response=create_data,
            delivery_response=delivery_data,
            pre_order_no=pre_order_no,
            error="" if success else f"RechargeDelivery returned code={delivery_data.get('code')}",
        )


@router.post("/task-cmd", response_model=SingleResponse)
async def task_cmd(req: TaskCmdRequest):
    return await send_single(SingleRequest(
        server=req.server,
        service="TaskSys",
        method="TestCmd",
        headers={"numid": req.numid, "areaid": req.areaid},
        body={"cmd": req.cmd, "task_id": req.task_id},
    ))
