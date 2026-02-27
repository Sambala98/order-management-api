from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.db.models import Order, User
from app.schemas.orders import OrderCreate, OrderOut, OrderStatusUpdate
from app.core.security import decode_access_token
from typing import Optional
from sqlalchemy import select, or_


router = APIRouter(prefix="/orders", tags=["orders"])
bearer = HTTPBearer()


def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer),
    db: Session = Depends(get_db),
) -> User:
    try:
        email = decode_access_token(creds.credentials)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    user = db.scalar(select(User).where(User.email == email))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


@router.post("", response_model=OrderOut, status_code=201)
def create_order(
    payload: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = Order(
        customer_name=payload.customer_name,
        item_name=payload.item_name,
        quantity=payload.quantity,
        user_id=current_user.id,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order



@router.get("", response_model=list[OrderOut])
def list_orders(
    search: Optional[str] = None,
    min_qty: Optional[int] = None,
    max_qty: Optional[int] = None,
    sort_by: str = "id",          # id | quantity | created_at
    sort_order: str = "desc",     # asc | desc
    limit: int = 20,
    offset: int = 0,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Safety limits
    if limit < 1:
        limit = 1
    if limit > 100:
        limit = 100
    if offset < 0:
        offset = 0

    stmt = select(Order)

    # RBAC filter
    if current_user.role != "admin":
        stmt = stmt.where(Order.user_id == current_user.id)

    # Search filter
    if search and search.strip():
        q = f"%{search.strip()}%"
        stmt = stmt.where(
            or_(
                Order.customer_name.ilike(q),
                Order.item_name.ilike(q),
            )
        )

    # Quantity filters
    if min_qty is not None:
        stmt = stmt.where(Order.quantity >= min_qty)
    if max_qty is not None:
        stmt = stmt.where(Order.quantity <= max_qty)

    # Sorting
    sort_map = {
        "id": Order.id,
        "quantity": Order.quantity,
        "created_at": Order.created_at,
    }
    col = sort_map.get(sort_by, Order.id)

    if sort_order.lower() == "asc":
        stmt = stmt.order_by(col.asc())
    else:
        stmt = stmt.order_by(col.desc())

    stmt = stmt.limit(limit).offset(offset)

    orders = db.scalars(stmt).all()
    return list(orders)

@router.get("/{order_id}", response_model=OrderOut)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.scalar(select(Order).where(Order.id == order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if current_user.role != "admin" and order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    return order

@router.patch("/{order_id}", response_model=OrderOut)
def update_order_status(
    order_id: int,
    payload: OrderStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    order = db.scalar(select(Order).where(Order.id == order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    is_owner = order.user_id == current_user.id
    is_admin = current_user.role == "admin"

    if not (is_owner or is_admin):
        raise HTTPException(status_code=403, detail="Not authorized")

    order.status = payload.status.value
    db.commit()
    db.refresh(order)
    return order


@router.delete("/{order_id}", status_code=204)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    _admin: User = Depends(require_admin),
):
    order = db.scalar(select(Order).where(Order.id == order_id))
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    db.delete(order)
    db.commit()
    return None