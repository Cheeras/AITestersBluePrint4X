from __future__ import annotations

import argparse
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from core.errors import AppError
from core.orchestrator import TestPlanOrchestrator
from core.settings import SettingsStore


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
TMP_DIR = BASE_DIR / ".tmp"
SETTINGS_STORE = SettingsStore(TMP_DIR / "settings.json")
ORCHESTRATOR = TestPlanOrchestrator(SETTINGS_STORE, TMP_DIR / "output")
MAX_BODY_BYTES = 64 * 1024


class ApplicationHandler(BaseHTTPRequestHandler):
    server_version = "JiraTestPlanCreator/1.0"

    def do_GET(self):
        path = urlparse(self.path).path
        if path == "/api/health":
            return self._json(200, {"ok": True, "status": "ready"})
        if path == "/api/settings":
            return self._handle(lambda: SETTINGS_STORE.public_view())
        static_files = {
            "/": "index.html",
            "/index.html": "index.html",
            "/styles.css": "styles.css",
            "/app.js": "app.js",
        }
        filename = static_files.get(path)
        if filename:
            return self._static(filename)
        return self._json(404, {"ok": False, "error": {"code": "NOT_FOUND", "message": "Route not found."}})

    def do_POST(self):
        path = urlparse(self.path).path
        routes = {
            "/api/settings": self._save_settings,
            "/api/connections/jira/test": ORCHESTRATOR.test_jira,
            "/api/connections/openrouter/test": ORCHESTRATOR.test_openrouter,
            "/api/generate": self._generate,
        }
        action = routes.get(path)
        if not action:
            return self._json(404, {"ok": False, "error": {"code": "NOT_FOUND", "message": "Route not found."}})
        self._handle(action)

    def log_message(self, format_string, *args):
        # Keep local logs useful without ever logging request bodies or headers.
        print(f"[{self.log_date_time_string()}] {self.client_address[0]} {format_string % args}")

    def _save_settings(self):
        return {"ok": True, "settings": SETTINGS_STORE.save(self._read_json())}

    def _generate(self):
        payload = self._read_json()
        return ORCHESTRATOR.generate(payload.get("prompt", ""))

    def _read_json(self) -> dict:
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError as exc:
            raise AppError("INVALID_REQUEST", "Invalid Content-Length header.") from exc
        if length <= 0 or length > MAX_BODY_BYTES:
            raise AppError("INVALID_REQUEST", "Request body is empty or too large.", 413)
        try:
            payload = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise AppError("INVALID_REQUEST", "Request body must be valid JSON.") from exc
        if not isinstance(payload, dict):
            raise AppError("INVALID_REQUEST", "Request body must be a JSON object.")
        return payload

    def _handle(self, action):
        try:
            result = action()
            if isinstance(result, dict) and "ok" not in result:
                result = {"ok": True, **result}
            self._json(200, result)
        except AppError as exc:
            self._json(exc.status, exc.as_dict())
        except Exception:
            self._json(500, {"ok": False, "error": {"code": "INTERNAL_ERROR", "message": "Unexpected local application error."}})

    def _json(self, status: int, payload: dict):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def _static(self, filename: str):
        path = STATIC_DIR / filename
        if not path.is_file():
            return self._json(404, {"ok": False, "error": {"code": "NOT_FOUND", "message": "File not found."}})
        data = path.read_bytes()
        content_type = mimetypes.guess_type(filename)[0] or "application/octet-stream"
        self.send_response(200)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Security-Policy", "default-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'")
        self.end_headers()
        self.wfile.write(data)


def main():
    parser = argparse.ArgumentParser(description="Run the local Jira Test Plan Creator.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", default=8765, type=int)
    args = parser.parse_args()
    server = ThreadingHTTPServer((args.host, args.port), ApplicationHandler)
    print(f"Jira Test Plan Creator running at http://{args.host}:{args.port}")
    print("Press Ctrl+C to stop.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
