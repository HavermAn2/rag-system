import logging
from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    AppError,
    FileNotFoundError,
    InvalidDocumentError,
    ExtractionError,
    VectorStoreError,
)

logger = logging.getLogger(__name__)

ERROR_STATUS = {
    FileNotFoundError: 404,
    InvalidDocumentError: 400,
    ExtractionError: 422,
    VectorStoreError: 503,
}


async def app_exception_handler(
    request: Request,
    exc: AppError,
):
    status_code = ERROR_STATUS.get(type(exc), 500)

    if status_code >= 500:
        logger.error(
            "Application error: %s",
            exc,
            exc_info=True,
        )

    return JSONResponse(
        status_code=status_code,
        content={
            "error": type(exc).__name__,
            "detail": (
                "Internal service error"
                if status_code >= 500
                else str(exc)
            ),
        },
    )