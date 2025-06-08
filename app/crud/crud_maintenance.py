# app/crud/crud_maintenance.py
import logging

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_inventory_partition(db: Session, year: int) -> dict:
    """
    Creates a new partition for the inventory_movement table for a specific year.
    This function is idempotent due to the 'IF NOT EXISTS' clause.
    """
    parent_table = "inventory_movement"
    partition_table_name = f"{parent_table}_y{year}"

    start_date = f"{year}-01-01 00:00:00+00"
    end_date = f"{year + 1}-01-01 00:00:00+00"

    # IMPORTANT: Use 'IF NOT EXISTS' to make this operation safe to re-run (idempotent)
    sql_command = text(
        f"""
        CREATE TABLE IF NOT EXISTS {partition_table_name}
        PARTITION OF {parent_table}
        FOR VALUES FROM ('{start_date}') TO ('{end_date}');
        """
    )

    try:
        db.execute(sql_command)
        db.commit()
        logger.info(
            f"Successfully created or verified existence of partition: {partition_table_name}"
        )
        return {
            "status": "success",
            "message": f"Partition '{partition_table_name}' created or already exists.",
        }
    except SQLAlchemyError as e:
        logger.error(f"Failed to create partition {partition_table_name}: {e}")
        db.rollback()
        return {
            "status": "error",
            "message": f"Could not create partition. Reason: {e}",
        }
