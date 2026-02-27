import time
import uuid
import logging
from fastapi import Request

logger = logging.getLogger("app")

async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    start = time.time()

    response = await call_next(request)

    duration_ms = (time.time() - start) * 1000
    logger.info(
        f"request_id={request_id} method={request.method} path={request.url.path} "
        f"status={response.status_code} duration_ms={duration_ms:.2f}"
    )
    response.headers["X-Request-Id"] = request_id
    return response