"""
Import all models here so that Alembic or other migration tools can detect them.
"""
from app.db.base_class import Base  # noqa
from app.models.user import User    # noqa
from app.models.product import Product  # noqa
from app.models.order import Order  # noqa