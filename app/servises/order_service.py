from sqlalchemy.orm import Session

from app.models.order import Order
from app.schemas.order import OrderCreate

def create_order(db: Session, order_in: OrderCreate) -> Order:
    db_order = Order(
        user_id=order_in.user_id,
        product_id=order_in.product_id,
        quantity=order_in.quantity,
        total_price=order_in.total_price
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def list_orders(db: Session) -> list[Order]:
    return db.query(Order).all()