from typing import List, TYPE_CHECKING
from sqlalchemy import String, Float, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.subject import Subject
    from app.models.daily_task import DailyTask

class Topic(Base):
    __tablename__ = "topics"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    estimated_hours: Mapped[float] = mapped_column(Float, nullable=False)

    subject: Mapped["Subject"] = relationship(back_populates="topics")
    daily_tasks: Mapped[List["DailyTask"]] = relationship(back_populates="topic")
