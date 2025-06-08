from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductCreate


def create_product(db: Session, *, product_in: ProductCreate) -> Product:
    db_product = Product(**product_in.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int) -> Product | None:
    return db.query(Product).filter(Product.id == product_id).first()


def get_low_stock_products(db: Session, threshold: int):
    return db.query(Product).filter(Product.quantity_in_stock < threshold).all()
