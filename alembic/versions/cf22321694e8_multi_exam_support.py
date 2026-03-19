"""multi exam support

Revision ID: cf22321694e8
Revises: 8327438b856f
Create Date: 2026-03-19 16:09:25.900888

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cf22321694e8'
down_revision: Union[str, None] = '8327438b856f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("PRAGMA foreign_keys=OFF")

    op.create_table(
        "user_exams_new",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("exam_id", sa.Integer(), nullable=False),
        sa.Column("exam_date", sa.Date(), nullable=False),
        sa.Column("study_hours_per_day", sa.Float(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["exam_id"], ["exams.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.execute(
        """
        INSERT INTO user_exams_new (
            id, user_id, exam_id, exam_date, study_hours_per_day, is_active, created_at
        )
        SELECT
            id, user_id, exam_id, exam_date, study_hours_per_day, 1, created_at
        FROM user_exams
        """
    )
    op.drop_table("user_exams")
    op.rename_table("user_exams_new", "user_exams")
    op.execute("PRAGMA foreign_keys=ON")


def downgrade() -> None:
    op.execute("PRAGMA foreign_keys=OFF")

    op.create_table(
        "user_exams_old",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("exam_id", sa.Integer(), nullable=False),
        sa.Column("exam_date", sa.Date(), nullable=False),
        sa.Column("study_hours_per_day", sa.Float(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["exam_id"], ["exams.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
    )
    op.execute(
        """
        INSERT INTO user_exams_old (
            id, user_id, exam_id, exam_date, study_hours_per_day, created_at
        )
        SELECT
            id, user_id, exam_id, exam_date, study_hours_per_day, created_at
        FROM user_exams
        """
    )
    op.drop_table("user_exams")
    op.rename_table("user_exams_old", "user_exams")
    op.execute("PRAGMA foreign_keys=ON")
