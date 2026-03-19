from datetime import datetime, date, timedelta
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional

class UserExamCreate(BaseModel):
    exam_id: int
    exam_date: date
    study_hours_per_day: float

    @field_validator("exam_date")
    @classmethod
    def exam_date_must_be_in_future(cls, v: date) -> date:
        if v <= date.today():
            raise ValueError("Exam date must be in the future (at least tomorrow)")
        return v

    @field_validator("study_hours_per_day")
    @classmethod
    def hours_must_be_valid(cls, v: float) -> float:
        if v <= 0 or v > 16:
            raise ValueError("Study hours per day must be between 0 and 16")
        return v

class UserExamResponse(BaseModel):
    id: int
    exam_id: int
    exam_date: date
    study_hours_per_day: float
    is_active: bool
    created_at: datetime
    days_remaining: int
    total_syllabus_hours: float
    required_hours_per_day: float
    model_config = ConfigDict(from_attributes=True)
