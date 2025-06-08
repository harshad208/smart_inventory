# app/schemas/maintenance.py
from pydantic import BaseModel, Field


class PartitionCreate(BaseModel):
    year: int = Field(
        ...,
        ge=2020,
        le=2050,
        description="The year to create an inventory partition for (e.g., 2026).",
    )
