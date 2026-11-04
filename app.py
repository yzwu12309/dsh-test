"""最简 Python Web 应用：一个返回 Hello World 的接口。"""

from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any


class HelloWorldHandler(BaseHTTPRequestHandler):
    """处理 GET /，返回 Hello World。"""

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path != "/":
            self._send_json(HTTPStatus.NOT_FOUND, {"error": "Not Found"})
            return
        self._send_json(HTTPStatus.OK, {"message": "Hello, World!"})

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
