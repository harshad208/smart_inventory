# app/schemas/product.py
from decimal import Decimal

from pydantic import BaseModel


# Shared properties
class ProductBase(BaseModel):
    sku: str
    name: str
    description: str | None = None
    price: Decimal
    quantity_in_stock: int = 0


# Properties to receive on item creation
class ProductCreate(ProductBase):
    pass


# Properties to return to client
class Product(ProductBase):
    id: int

    class Config:
        from_attributes = True  # This allows Pydantic to read data from ORM models
