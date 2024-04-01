from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "12a6a09b05a0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "File_Table",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("path", sa.String(), nullable=False),
        sa.Column("time", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False, ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "User_Table",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_name", sa.String(), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("date_register", sa.DateTime(), server_default=sa.text("CURRENT_TIMESTAMP"), nullable=False, ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
        sa.UniqueConstraint("user_name"),
    )


def downgrade() -> None:
    op.drop_table("User_Table")
    op.drop_table("File_Table")
