"""
Standardized API Error Handlers and Custom Exceptions
Day 65 Implementation: Enhanced error recovery, machine-readable error codes, and remediation hints.
"""

from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
from typing import Optional, Dict, Any


class ZecpathAPIException(Exception):
    """Base custom application exception with error codes and remediation hints."""
    def __init__(
        self,
        message: str,
        error_code: str = "GENERIC_API_ERROR",
        status_code: int = 400,
        remediation_hint: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.remediation_hint = remediation_hint or "Verify request payload and parameters."
        self.details = details or {}


class ResourceNotFoundException(ZecpathAPIException):
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            message=f"{resource} with identifier '{identifier}' was not found.",
            error_code="RESOURCE_NOT_FOUND",
            status_code=404,
            remediation_hint="Verify the requested ID exists in the database."
        )


class ModelInferenceException(ZecpathAPIException):
    def __init__(self, model_name: str, reason: str):
        super().__init__(
            message=f"AI model inference failed for '{model_name}': {reason}",
            error_code="MODEL_INFERENCE_FAILURE",
            status_code=502,
            remediation_hint="Retry request or use fallback scoring rule."
        )


async def api_error_handler(request: Request, exc: Exception):
    """Global exception handler returning structured, actionable error payloads."""
    timestamp = datetime.now(timezone.utc).isoformat()
    
    if isinstance(exc, ZecpathAPIException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_code": exc.error_code,
                "message": exc.message,
                "remediation_hint": exc.remediation_hint,
                "details": exc.details,
                "path": request.url.path,
                "timestamp": timestamp
            }
        )

    if isinstance(exc, HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error_code": f"HTTP_{exc.status_code}",
                "message": exc.detail if isinstance(exc.detail, str) else "HTTP request failed.",
                "remediation_hint": "Inspect request parameters or authorization header.",
                "path": request.url.path,
                "timestamp": timestamp
            }
        )

    # General unexpected exceptions
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error_code": "INTERNAL_SERVER_ERROR",
            "message": str(exc) if str(exc) else "An unexpected internal server error occurred.",
            "remediation_hint": "Check server telemetry or contact system administrator.",
            "path": request.url.path,
            "timestamp": timestamp
        }
    )