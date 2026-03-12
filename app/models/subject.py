from typing import List, TYPE_CHECKING
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

if TYPE_CHECKING:
    from app.models.exam import Exam
    from app.models.topic import Topic

class Subject(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    exam_id: Mapped[int] = mapped_column(ForeignKey("exams.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    exam: Mapped["Exam"] = relationship(back_populates="subjects")
    topics: Mapped[List["Topic"]] = relationship(back_populates="subject")
