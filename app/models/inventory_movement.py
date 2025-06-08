import datetime
import enum

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from app.db.base import Base


class MovementType(str, enum.Enum):
    RESTOCK = "restock"
    SALE = "sale"
    RETURN = "return"
    ADJUSTMENT = "adjustment"


class InventoryMovement(Base):
    __tablename__ = "inventory_movement"

    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("product.id"), nullable=False, index=True
    )
    quantity_changed: Mapped[int] = mapped_column(nullable=False)
    movement_type: Mapped[MovementType] = mapped_column(
        Enum(MovementType), nullable=False
    )
    timestamp: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
