from fastapi import FastAPI

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.middleware import request_logging_middleware
from app.core.limiter import limiter

from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.api.routes.auth import router as auth_router
from app.api.routes.orders import router as orders_router

app = FastAPI(title=settings.APP_NAME)

setup_logging()
app.middleware("http")(request_logging_middleware)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# include routers correctly
app.include_router(auth_router)
app.include_router(orders_router)

@app.get("/health")
def health():
    return {"status": "ok"}