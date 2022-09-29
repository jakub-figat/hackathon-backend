"""

Revision ID: bab96c6e65c9
Revises: e567f4b93108
Create Date: 2022-10-03 21:55:15.192470

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op


# revision identifiers, used by Alembic.
revision = "bab96c6e65c9"
down_revision = "e567f4b93108"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "refreshtokenmodels",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.Column("user_id", postgresql.UUID(), nullable=True),
        sa.Column("jti", postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["usermodels.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_refreshtokenmodels_id"), "refreshtokenmodels", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_refreshtokenmodels_id"), table_name="refreshtokenmodels")
    op.drop_table("refreshtokenmodels")
    # ### end Alembic commands ###
