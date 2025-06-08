from app.db.base import Base

from .inventory_movement import InventoryMovement
from .order import Order, OrderItem
from .product import Product
# Import all models here so that Base has them registered
# and so that SQLAlchemy can resolve all relationships.
from .supplier import Supplier
