from typing import List
from datetime import date
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.schemas.progress import DashboardResponse, EndOfDayResponse, SnapshotResponse
from app.utils.dependencies import get_current_user
from app.services import progress_service

router = APIRouter(prefix="/progress", tags=["progress"])

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return progress_service.get_dashboard_data(db, current_user.id)

@router.post("/end-of-day", response_model=EndOfDayResponse)
def end_of_day(
    target_date: date = Query(default_factory=date.today),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return progress_service.generate_end_of_day(db, current_user.id, target_date)

@router.get("/history", response_model=List[SnapshotResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return progress_service.get_progress_history(db, current_user.id)

@router.post("/trigger-reminders", tags=["progress"])
def trigger_reminders(current_user: User = Depends(get_current_user)):
    """
    Manually trigger the reminder check.
    Used for testing — in production this runs on schedule.
    """
    from app.services.notification_service import send_reminders_for_all_users
    send_reminders_for_all_users()
    return {"message": "Reminder check completed"}
