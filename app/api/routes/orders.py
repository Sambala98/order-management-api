from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.db.models import Order
from app.schemas.orders import OrderCreate, OrderOut
from app.core.security import decode_access_token

router = APIRouter(prefix="/orders", tags=["orders"])
bearer = HTTPBearer()


def require_user_email(creds: HTTPAuthorizationCredentials = Depends(bearer)) -> str:
    try:
        return decode_access_token(creds.credentials)
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


@router.post("", response_model=OrderOut, status_code=201)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    _user: str = Depends(require_user_email),
):
    order = Order(
        customer_name=payload.customer_name,
        item_name=payload.item_name,
        quantity=payload.quantity,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


@router.get("", response_model=list[OrderOut])
def list_orders(
    db: Session = Depends(get_db),
    _user: str = Depends(require_user_email),
):
    orders = db.scalars(select(Order).order_by(Order.id.desc())).all()
    return list(orders)


@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    _user: str = Depends(require_user_email),
):
    order = db.scalar(select(Order).where(Order.id == order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    _user: str = Depends(require_user_email),
):
    order = db.scalar(select(Order).where(Order.id == order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    db.delete(order)
    db.commit()
    return None