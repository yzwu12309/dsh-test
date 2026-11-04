"""app.py 的接口测试。"""

from __future__ import annotations

import json
import threading
import unittest
from http.client import HTTPConnection

from app import create_server


class HelloWorldApiTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.server = create_server(port=0)
        cls.port = cls.server.server_address[1]
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def request(self, path: str) -> tuple[int, str | None, bytes]:
        connection = HTTPConnection("127.0.0.1", self.port, timeout=2)
        try:
            connection.request("GET", path)
            response = connection.getresponse()
            return (
                response.status,
                response.getheader("Content-Type"),
                response.read(),
            )
        finally:
            connection.close()

    def test_hello_world(self) -> None:
        status, content_type, body = self.request("/")

        self.assertEqual(status, 200)
        self.assertEqual(content_type, "application/json; charset=utf-8")
        self.assertEqual(json.loads(body), {"message": "Hello, World!"})

    def test_unknown_path_returns_404(self) -> None:
        status, _, body = self.request("/missing")

        self.assertEqual(status, 404)
        self.assertEqual(json.loads(body), {"error": "Not Found"})


if __name__ == "__main__":
    unittest.main()
