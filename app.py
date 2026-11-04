"""最简 Python Web 应用：Hello World 与取消工单 mock 接口。"""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import unquote


class HelloWorldHandler(BaseHTTPRequestHandler):
    """处理 Hello World 与取消工单 mock 接口。"""

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path != "/":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not Found"})
            return
        self._send_json(HTTPStatus.OK, {"message": "Hello, World!"})

    def do_POST(self) -> None:
        path = self.path.split("?", 1)[0].strip("/")
        parts = path.split("/") if path else []
        if (
            len(parts) == 3
            and parts[0] == "tickets"
            and parts[1]
            and parts[2] == "cancel"
        ):
            ticket_id = unquote(parts[1])
            self._send_json(
                HTTPStatus.OK,
                {"ticket_id": ticket_id, "status": "cancelled"},
            )
            return
        self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not Found"})

    def _send_json(self, status: HTTPStatus, payload: dict[str, Any]) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


def create_server(host: str = "127.0.0.1", port: int = 8000) -> ThreadingHTTPServer:
    """创建 HTTP 服务器；传入 port=0 时由系统分配空闲端口。"""
    return ThreadingHTTPServer((host, port), HelloWorldHandler)


def main() -> None:
    server = create_server()
    host, port = server.server_address[:2]
    print(f"服务已启动：http://{host}:{port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
