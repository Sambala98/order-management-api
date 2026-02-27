from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.db.models import User
from app.schemas.auth import UserCreate, Token
from app.core.security import hash_password, verify_password, create_access_token
from app.core.limiter import limiter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", status_code=201)
@limiter.limit("3/minute")
def register(request: Request, payload: UserCreate, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(User.email == payload.email))
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user = User(email=payload.email, hashed_password=hash_password(payload.password))
    db.add(user)
    db.commit()
    return {"message": "registered"}


@router.post("/login", response_model=Token)
@limiter.limit("5/minute")
def login(request: Request, payload: UserCreate, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.email == payload.email))
    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token = create_access_token(subject=user.email)
    return Token(access_token=token)