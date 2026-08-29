from __future__ import annotations

import json
import urllib.error
import urllib.request
from dataclasses import dataclass


@dataclass
class HttpResponse:
    status: int
    body: bytes
    headers: dict[str, str]

    def json(self):
        return json.loads(self.body.decode("utf-8"))


class TransportError(Exception):
    pass


class UrlLibTransport:
    def request(
        self,
        method: str,
        url: str,
        headers: dict[str, str] | None = None,
        json_body: dict | None = None,
        timeout: float = 20,
    ) -> HttpResponse:
        data = None
        request_headers = dict(headers or {})
        if json_body is not None:
            data = json.dumps(json_body, ensure_ascii=False).encode("utf-8")
            request_headers["Content-Type"] = "application/json"
        request = urllib.request.Request(url, data=data, headers=request_headers, method=method)
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                return HttpResponse(response.status, response.read(), dict(response.headers.items()))
        except urllib.error.HTTPError as exc:
            return HttpResponse(exc.code, exc.read(), dict(exc.headers.items()) if exc.headers else {})
        except (urllib.error.URLError, TimeoutError, OSError) as exc:
            raise TransportError(str(exc.reason) if isinstance(exc, urllib.error.URLError) else str(exc)) from exc
