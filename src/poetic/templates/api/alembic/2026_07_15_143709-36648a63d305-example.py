"""example

Revision ID: 36648a63d305
Revises:
Create Date: 2026-07-15 14:37:09.521278

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from alembic_migrations.alembdantic import opd
from alembic_migrations.models import ExampleTable

# revision identifiers, used by Alembic.
revision: str = "36648a63d305"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    opd.create_table(ExampleTable)


def downgrade() -> None:
    """Downgrade schema."""
    opd.drop_table(ExampleTable)
