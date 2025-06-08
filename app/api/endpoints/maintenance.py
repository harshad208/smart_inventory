# app/api/endpoints/maintenance.py
from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.crud import crud_maintenance
from app.schemas.maintenance import PartitionCreate

# In a real app, you would have a dependency that gets the current superuser
# from app.api.deps import get_current_active_superuser
# from app.models.user import User

router = APIRouter()


@router.post("/partitions/inventory", status_code=201)
def create_new_inventory_partition(
    *,
    db: Session = Depends(deps.get_db),
    partition_in: PartitionCreate = Body(...),
    # ------------------  IMPORTANT SECURITY NOTE ------------------
    # In a real application, you would UNCOMMENT the line below.
    # This endpoint MUST be protected and only accessible by an admin/superuser.
    # current_user: User = Depends(get_current_active_superuser),
    # ----------------------------------------------------------------
):
    """
    Create a new partition for the inventory_movement table for a given year.
    This is an administrative action and must be protected.
    """
    result = crud_maintenance.create_inventory_partition(db=db, year=partition_in.year)

    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])

    return result
