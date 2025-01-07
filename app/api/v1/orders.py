from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.order import OrderCreate, OrderRead
from app.services.order_service import create_order, list_orders

router = APIRouter()

@router.post("/", response_model=OrderRead)
def create_new_order(order_in: OrderCreate, db: Session = Depends(get_db)):
    """
    Create order
    """
    return create_order(db, order_in)

@router.get("/", response_model=list[OrderRead])
def get_all_orders(db: Session = Depends(get_db)):
    """
    Get list of all orders
    """
    return list_orders(db)