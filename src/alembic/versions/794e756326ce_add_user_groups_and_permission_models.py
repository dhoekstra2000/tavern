"""Add user groups and permission models

Revision ID: 794e756326ce
Revises: 82fa26df03d2
Create Date: 2022-10-07 20:50:13.699458

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "794e756326ce"
down_revision = "82fa26df03d2"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "permission",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=True),
        sa.Column("date_updated", sa.DateTime(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "usergroup",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("date_created", sa.DateTime(), nullable=True),
        sa.Column("date_updated", sa.DateTime(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("superuser", sa.Boolean(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "group_permission_association",
        sa.Column("group_id", sa.Integer(), nullable=True),
        sa.Column("permission_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["usergroup.id"],
        ),
        sa.ForeignKeyConstraint(
            ["permission_id"],
            ["permission.id"],
        ),
    )
    op.add_column("user", sa.Column("group_id", sa.Integer(), nullable=True))
    op.create_foreign_key(None, "user", "usergroup", ["group_id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "user", type_="foreignkey")
    op.drop_column("user", "group_id")
    op.drop_table("group_permission_association")
    op.drop_table("usergroup")
    op.drop_table("permission")
    # ### end Alembic commands ###
