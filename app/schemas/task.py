from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, field_validator

class DailyTaskCreate(BaseModel):
    topic_id: int
    task_date: date
    planned_hours: float

    @field_validator("planned_hours")
    @classmethod
    def hours_must_be_positive(cls, v):
        if v <= 0 or v > 16:
            raise ValueError("planned_hours must be between 0 and 16")
        return v

class TaskLogUpdate(BaseModel):
    actual_hours: Optional[float] = None
    status: str  # "COMPLETED" or "SKIPPED"

    @field_validator("status")
    @classmethod
    def status_must_be_valid(cls, v):
        if v not in ("COMPLETED", "SKIPPED"):
            raise ValueError("status must be COMPLETED or SKIPPED")
        return v

    @field_validator("actual_hours")
    @classmethod
    def actual_hours_must_be_positive(cls, v):
        if v is not None and (v < 0 or v > 16):
            raise ValueError("actual_hours must be between 0 and 16")
        return v

class TaskLogResponse(BaseModel):
    id: int
    actual_hours: Optional[float]
    status: str
    updated_at: datetime
    model_config = ConfigDict(from_attributes=True)

class DailyTaskResponse(BaseModel):
    id: int
    topic_id: int
    topic_name: str      # denormalized for convenience
    subject_name: str    # denormalized for convenience
    task_date: date
    planned_hours: float
    task_log: Optional[TaskLogResponse] = None
    model_config = ConfigDict(from_attributes=True)
