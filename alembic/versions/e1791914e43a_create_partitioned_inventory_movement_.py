"""Create partitioned inventory_movement table

Revision ID: e1791914e43a
Revises: c3c05607b95b
Create Date: 2025-06-08 20:41:28.408627

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e1791914e43a"
down_revision: Union[str, None] = "c3c05607b95b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create an ENUM type for movement_type
    op.execute(
        """
        CREATE TYPE movementtype AS ENUM ('restock', 'sale', 'return', 'adjustment');
    """
    )

    # 1. Create the main (parent) partitioned table
    op.execute(
        """
        CREATE TABLE inventory_movement (
            id SERIAL,
            product_id INTEGER NOT NULL,
            quantity_changed INTEGER NOT NULL,
            movement_type MOVEMENTTYPE NOT NULL,
            timestamp TIMESTAMPTZ NOT NULL DEFAULT now(),
            PRIMARY KEY (id, timestamp) -- Partition key MUST be part of the primary key
        ) PARTITION BY RANGE (timestamp);
    """
    )
    op.create_foreign_key(
        "fk_inventory_movement_product_id",
        "inventory_movement",
        "product",
        ["product_id"],
        ["id"],
    )

    # 2. Create the first partition for the current year
    op.execute(
        """
        CREATE TABLE inventory_movement_y2024 PARTITION OF inventory_movement
        FOR VALUES FROM ('2024-01-01 00:00:00+00') TO ('2025-01-01 00:00:00+00');
    """
    )
    # Create another partition for next year
    op.execute(
        """
        CREATE TABLE inventory_movement_y2025 PARTITION OF inventory_movement
        FOR VALUES FROM ('2025-01-01 00:00:00+00') TO ('2026-01-01 00:00:00+00');
    """
    )


def downgrade() -> None:
    op.drop_table("inventory_movement_y2025")
    op.drop_table("inventory_movement_y2024")
    op.drop_table("inventory_movement")
    op.execute("DROP TYPE movementtype;")
