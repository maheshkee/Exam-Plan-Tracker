from datetime import date
from typing import TYPE_CHECKING
from sqlalchemy import String, Float, ForeignKey, Date, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.user_exam import UserExam

class ProgressSnapshot(Base):
    __tablename__ = "progress_snapshots"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_exam_id: Mapped[int] = mapped_column(ForeignKey("user_exams.id"), nullable=False)
    snapshot_date: Mapped[date] = mapped_column(Date, nullable=False)
    topics_completed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    hours_completed: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    pace_status: Mapped[str] = mapped_column(String(20), nullable=False) # "AHEAD", "ON_TRACK", "BEHIND"

    user_exam: Mapped["UserExam"] = relationship(back_populates="progress_snapshots")
