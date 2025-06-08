from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Order, OrderItem, Product, Supplier


def get_pending_orders_summary(db: Session):
    """
    Generates a report of pending orders grouped by supplier.
    """
    results = (
        db.query(
            Supplier.name.label("supplier_name"),
            func.count(Order.id).label("pending_orders_count"),
        )
        # Start with Supplier and join "outwards"
        .join(Supplier.products)  # Joins Supplier to Product using the relationship
        .join(Product.order_items)  # Joins Product to OrderItem
        .join(OrderItem.order)  # Joins OrderItem to Order
        .filter(Order.status == "pending")
        .group_by(Supplier.name)
        .all()
    )
    return results
