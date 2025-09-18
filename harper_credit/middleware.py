import json
import logging
import time
import uuid
from datetime import datetime, timezone
from typing import Callable

from django.http import HttpRequest, HttpResponse


ACCESS_LOGGER = logging.getLogger("access")


def _utc_iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class RequestIDMiddleware:
    """Propagate X-Request-ID from header or generate one and echo in responses."""

    header_name = "HTTP_X_REQUEST_ID"
    response_header = "X-Request-ID"

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        request_id = request.META.get(self.header_name)
        if not request_id:
            request_id = str(uuid.uuid4())
        request.request_id = request_id

        try:
            response = self.get_response(request)
        except Exception:
            # Ensure header on error paths too
            response = HttpResponse(status=500)
            raise
        finally:
            # Always attach header to response if available
            try:
                response[self.response_header] = request.request_id  # type: ignore[attr-defined]
            except Exception:
                pass

        return response


class AccessLogMiddleware:
    """Emit a single JSON access log line per request/response."""

    def __init__(self, get_response: Callable[[HttpRequest], HttpResponse]):
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        start = time.perf_counter()
        try:
            response = self.get_response(request)
            return response
        finally:
            duration_ms = int((time.perf_counter() - start) * 1000)
            path = request.get_full_path() if hasattr(request, "get_full_path") else ""
            user_agent = request.META.get("HTTP_USER_AGENT", "")
            # Common client IP headers
            client_ip = (
                request.META.get("HTTP_X_FORWARDED_FOR", "").split(",")[0].strip()
                or request.META.get("REMOTE_ADDR", "")
            )
            status_code = None
            try:
                status_code = getattr(response, "status_code", None)  # type: ignore[name-defined]
            except Exception:
                status_code = None
            log = {
                "timestamp": _utc_iso_now(),
                "level": "INFO",
                "logger": "access",
                "method": request.method,
                "path": path,
                "status_code": status_code,
                "duration_ms": duration_ms,
                "request_id": getattr(request, "request_id", None),
                "client_ip": client_ip or None,
                "user_agent": user_agent or None,
            }
            try:
                ACCESS_LOGGER.info(json.dumps(log, separators=(",", ":")))
            except Exception:
                # best-effort logging; never break request flow
                pass


