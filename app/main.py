from fastapi import FastAPI
from app.core.config import settings
from app.api import api_router
from app.db.models import Base
from app.db.session import engine
from app.core.logging import setup_logging
from app.core.middleware import request_logging_middleware

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from app.core.limiter import limiter

app = FastAPI(title=settings.APP_NAME)

setup_logging()
app.middleware("http")(request_logging_middleware)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

@app.on_event("startup")
def on_startup():
    # Base.metadata.create_all(bind=engine)

 app.include_router(api_router)

@app.get("/health")
def health():
    return {"status": "ok"}