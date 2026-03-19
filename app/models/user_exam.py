from datetime import datetime, date
from typing import List, TYPE_CHECKING
from sqlalchemy import ForeignKey, Date, DateTime, Float, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.user import User
    from app.models.exam import Exam
    from app.models.daily_task import DailyTask
    from app.models.progress_snapshot import ProgressSnapshot
    from app.models.notification_log import NotificationLog

class UserExam(Base):
    __tablename__ = "user_exams"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), nullable=False)
    exam_date: Mapped[date] = mapped_column(Date, nullable=False)
    study_hours_per_day: Mapped[float] = mapped_column(Float, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    user: Mapped["User"] = relationship(back_populates="user_exams")
    exam: Mapped["Exam"] = relationship(back_populates="user_exams")
    daily_tasks: Mapped[List["DailyTask"]] = relationship(back_populates="user_exam")
    progress_snapshots: Mapped[List["ProgressSnapshot"]] = relationship(back_populates="user_exam")
    notification_logs: Mapped[List["NotificationLog"]] = relationship(back_populates="user_exam")
