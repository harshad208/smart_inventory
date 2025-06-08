from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_supplier
from app.schemas.supplier import Supplier, SupplierCreate

router = APIRouter()


@router.post("/", response_model=Supplier)
def create_supplier(
    *,
    db: Session = Depends(deps.get_db),
    supplier_in: SupplierCreate,
):
    """
    Create new supplier.
    """
    supplier = crud_supplier.create_supplier(db=db, supplier=supplier_in)
    return supplier


@router.get("/", response_model=List[Supplier])
def read_suppliers(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retrieve suppliers.
    """
    suppliers = crud_supplier.get_suppliers(db, skip=skip, limit=limit)
    return suppliers
