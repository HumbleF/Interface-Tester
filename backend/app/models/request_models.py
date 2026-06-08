from pydantic import BaseModel


class TargetServer(BaseModel):
    host: str = "127.0.0.1"
    port: int = 14354


class SingleRequest(BaseModel):
    server: TargetServer = TargetServer()
    service: str
    method: str
    headers: dict[str, str] = {}
    body: dict = {}


class ConcurrentRequest(BaseModel):
    server: TargetServer = TargetServer()
    service: str
    method: str
    user_ids: list[str]
    areaid: str = "5016"
    body: dict = {}


class SingleResponse(BaseModel):
    status_code: int
    body: dict
    elapsed_ms: float


class ConcurrentResponseItem(BaseModel):
    numid: str
    status_code: int
    body: dict
    elapsed_ms: float
    error: str = ""


class ConcurrentResponse(BaseModel):
    total: int
    results: list[ConcurrentResponseItem]
    total_elapsed_ms: float


class MockPurchaseRequest(BaseModel):
    server: TargetServer = TargetServer()
    numid: str
    areaid: str = "5016"
    product_id: int
    event: int = 1


class MockPurchaseResponse(BaseModel):
    success: bool
    create_response: dict = {}
    delivery_response: dict = {}
    pre_order_no: str = ""
    error: str = ""


class TaskCmdRequest(BaseModel):
    server: TargetServer = TargetServer()
    numid: str
    areaid: str = "5016"
    cmd: str
    task_id: list[int]
