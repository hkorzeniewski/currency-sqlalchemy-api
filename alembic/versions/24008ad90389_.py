"""empty message

Revision ID: 24008ad90389
Revises: 9825036cb991
Create Date: 2023-12-13 11:07:56.297305

"""
import sqlalchemy as sa
import sqlmodel

from alembic import op

# revision identifiers, used by Alembic.
revision = "24008ad90389"
down_revision = "9825036cb991"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "currency",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("eur_pln", sa.Numeric(precision=6, scale=4), nullable=False),
        sa.Column("usd_pln", sa.Numeric(precision=6, scale=4), nullable=False),
        sa.Column("chf_pln", sa.Numeric(precision=6, scale=4), nullable=False),
        sa.Column("eur_usd", sa.Numeric(precision=6, scale=4), nullable=False),
        sa.Column("chf_usd", sa.Numeric(precision=6, scale=4), nullable=False),
        sa.Column("rate_date", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("currency")
    # ### end Alembic commands ###
