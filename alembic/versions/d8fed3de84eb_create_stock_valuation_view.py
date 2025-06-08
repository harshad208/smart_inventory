"""Create stock valuation view

Revision ID: d8fed3de84eb
Revises: c5650216bf89
Create Date: 2025-06-08 19:46:20.258355

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "d8fed3de84eb"
down_revision: Union[str, None] = "c5650216bf89"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


view_name = "vw_stock_valuation"
view_query = """
CREATE VIEW {0} AS
 SELECT p.id,
    p.name,
    p.sku,
    p.price,
    p.quantity_in_stock,
    p.price * p.quantity_in_stock AS valuation
   FROM product p;
""".format(
    view_name
)


def upgrade() -> None:
    op.execute(view_query)


def downgrade() -> None:
    op.execute(f"DROP VIEW {view_name};")
