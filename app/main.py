from fastapi import FastAPI
from app.core.config import settings
from app.api import api_router
from app.db.models import Base
from app.db.session import engine

app = FastAPI(title=settings.APP_NAME)

Base.metadata.create_all(bind=engine)

app.include_router(api_router)

@app.get("/health")
def health():
    return {"status": "ok"}