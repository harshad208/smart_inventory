# app/api/endpoints/products.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_product
from app.schemas.product import Product, ProductCreate

router = APIRouter()


@router.post("/", response_model=Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: ProductCreate,
):
    """
    Create new product.
    """
    product = crud_product.create_product(db=db, product_in=product_in)
    return product


@router.get("/{product_id}", response_model=Product)
def read_product(
    *,
    db: Session = Depends(deps.get_db),
    product_id: int,
):
    """
    Get product by ID.
    """
    product = crud_product.get_product(db=db, product_id=product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
