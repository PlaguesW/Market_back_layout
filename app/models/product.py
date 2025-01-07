from sqlalchemy import Column, Integer, String, Float
from app.db.base_class import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    brand = Column(String, nullable=True)
    article_number = Column(String, index=True, nullable=True)
    price = Column(Float, nullable=False, default=0.0)