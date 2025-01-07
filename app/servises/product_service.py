from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate

def create_product(db: Session, product_in: ProductCreate) -> Product:
    db_product = Product(
        name=product_in.name,
        brand=product_in.brand,
        article_number=product_in.article_number,
        price=product_in.price
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def get_products(db: Session) -> list[Product]:
    return db.query(Product).all()