from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "32a6c74f9f19"
down_revision: Union[str, Sequence[str], None] = "37f8c25bf8b2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("author", sa.String(length=150), nullable=False),
        sa.Column("isbn", sa.String(length=13), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("added_by_id", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default="now()",
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default="now()",
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["added_by_id"], ["users.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("isbn"),
    )


def downgrade() -> None:
    op.drop_table("books")
