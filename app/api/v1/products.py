from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.product import ProductCreate, ProductRead
from app.services.product_service import create_product, get_products

router = APIRouter()

@router.post("/", response_model=ProductRead)
def create_new_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    """
    Create a new goods (parts)
    """
    return create_product(db, product_in)

@router.get("/", response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    """
    Get list of all parts
    """
    return get_products(db)