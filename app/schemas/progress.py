from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class DashboardResponse(BaseModel):
    # Enrollment info
    exam_name: str
    exam_date: date
    days_remaining: int

    # Syllabus progress
    total_topics: int
    topics_completed: int
    completion_percentage: float   # 0.0 to 100.0, rounded to 1 decimal

    # Pace tracking
    total_syllabus_hours: float
    hours_studied: float
    required_hours_per_day: float
    actual_hours_per_day: float    # hours_studied / days_elapsed (0 if day 0)
    pace_status: str               # "AHEAD", "ON_TRACK", "BEHIND"

    # Today
    tasks_today: int               # total tasks planned for today
    tasks_completed_today: int     # tasks with status COMPLETED today

class SnapshotResponse(BaseModel):
    id: int
    snapshot_date: date
    topics_completed: int
    hours_completed: float
    pace_status: str
    model_config = ConfigDict(from_attributes=True)

class EndOfDayResponse(BaseModel):
    snapshot_date: date
    tasks_planned: int
    tasks_completed: int
    tasks_skipped: int
    tasks_pending: int             # planned but no log yet
    hours_planned: float
    hours_completed: float
    day_status: str                # "COMPLETED", "PARTIAL", "MISSED"
    pace_status: str
