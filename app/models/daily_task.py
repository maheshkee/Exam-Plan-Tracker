from datetime import date
from typing import Optional, TYPE_CHECKING
from sqlalchemy import ForeignKey, Date, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.user_exam import UserExam
    from app.models.topic import Topic
    from app.models.task_log import TaskLog

class DailyTask(Base):
    __tablename__ = "daily_tasks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_exam_id: Mapped[int] = mapped_column(ForeignKey("user_exams.id"), nullable=False)
    topic_id: Mapped[int] = mapped_column(ForeignKey("topics.id"), nullable=False)
    task_date: Mapped[date] = mapped_column(Date, nullable=False)
    planned_hours: Mapped[float] = mapped_column(Float, nullable=False)

    user_exam: Mapped["UserExam"] = relationship(back_populates="daily_tasks")
    topic: Mapped["Topic"] = relationship(back_populates="daily_tasks")
    task_log: Mapped[Optional["TaskLog"]] = relationship(back_populates="daily_task")
