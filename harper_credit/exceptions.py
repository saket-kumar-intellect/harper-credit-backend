import json
import logging
from typing import Any, Dict

from django.conf import settings
from django.http import HttpRequest, JsonResponse
from django.utils.deprecation import MiddlewareMixin
from rest_framework.views import exception_handler as drf_exception_handler

LOGGER = logging.getLogger("errors")


def problem_json(request: HttpRequest, status: int, error: str, message: str, details: Any | None = None) -> JsonResponse:
    payload: Dict[str, Any] = {
        "request_id": getattr(request, "request_id", None),
        "status": status,
        "error": error,
        "message": message,
    }
    if details is not None:
        payload["details"] = details
    return JsonResponse(payload, status=status, content_type="application/json")


def global_exception_handler(exc, context):
    """DRF exception handler that emits JSON consistently and logs errors."""
    request: HttpRequest = context.get("request")
    response = drf_exception_handler(exc, context)
    if response is not None:
        # Standard DRF errors (e.g., validation) -> 400 etc.
        try:
            details = response.data
        except Exception:
            details = None
        # Normalize error name
        error_name = getattr(exc, "__class__", type(exc)).__name__
        return problem_json(request, response.status_code, error_name, "Bad Request", details)

    # Non-DRF uncaught exceptions -> 500
    LOGGER.exception("Unhandled exception", exc_info=exc)
    if settings.DEBUG:
        # In DEBUG, let Django default to HTML for developer ergonomics.
        return None
    return problem_json(request, 500, "InternalServerError", "An unexpected error occurred")


class JsonErrorMiddleware(MiddlewareMixin):
    """Ensure Django Http404/PermissionDenied and other errors return JSON in non-DEBUG."""

    def process_exception(self, request: HttpRequest, exception):
        from django.http import Http404
        from django.core.exceptions import PermissionDenied

        if settings.DEBUG:
            return None

        if isinstance(exception, Http404):
            return problem_json(request, 404, "NotFound", "The requested resource was not found")
        if isinstance(exception, PermissionDenied):
            return problem_json(request, 403, "Forbidden", "You do not have permission to access this resource")
        # Other exceptions handled by DRF handler or default 500 path
        return None


