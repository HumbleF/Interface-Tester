import json
import socket
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.config import settings

FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_proto_path() -> Path:
    return FIXTURES_DIR / "award_hub_cli.proto"


@pytest.fixture
def unused_tcp_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


@pytest.fixture(autouse=True)
def clean_dirs(tmp_path):
    original_upload = settings.upload_dir
    original_compiled = settings.compiled_dir
    original_config = settings.config_dir
    settings.upload_dir = tmp_path / "uploads"
    settings.compiled_dir = tmp_path / "compiled"
    settings.config_dir = tmp_path / "configs"
    settings.upload_dir.mkdir()
    settings.compiled_dir.mkdir()
    settings.config_dir.mkdir()
    yield
    settings.upload_dir = original_upload
    settings.compiled_dir = original_compiled
    settings.config_dir = original_config


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as c:
        yield c


class MockGameHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length)) if content_length else {}
        response = {
            "code": 0,
            "data": {
                "numid": self.headers.get("numid", ""),
                "path": self.path,
                "body": body,
            },
        }
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        pass


class MockPurchaseHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = json.loads(self.rfile.read(content_length)) if content_length else {}

        if self.path == "/Product/RechargeCreate":
            response = {
                "code": 0,
                "data": {"pre_order_no": "MOCK_TEST_ORDER_001"},
            }
        elif self.path == "/Product/RechargeDelivery":
            response = {
                "code": 0,
                "data": {"pre_order_no": body.get("pre_order_no", "")},
            }
        else:
            response = {
                "code": 0,
                "data": {"numid": self.headers.get("numid", ""), "path": self.path, "body": body},
            }

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def log_message(self, format, *args):
        pass


@pytest.fixture
def mock_game_server(unused_tcp_port):
    server = HTTPServer(("127.0.0.1", unused_tcp_port), MockGameHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield unused_tcp_port
    server.shutdown()


@pytest.fixture
def mock_purchase_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    server = HTTPServer(("127.0.0.1", port), MockPurchaseHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    yield port
    server.shutdown()
