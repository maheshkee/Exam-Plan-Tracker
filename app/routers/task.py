from typing import List
from datetime import date
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models.user import User
from app.models.daily_task import DailyTask
from app.models.topic import Topic
from app.schemas.task import DailyTaskCreate, DailyTaskResponse, TaskLogUpdate, TaskLogResponse
from app.utils.dependencies import get_current_user
from app.services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.post("", response_model=DailyTaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    data: DailyTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_task = task_service.create_daily_task(db, current_user.id, data)
    
    # Re-fetch with joinedload to build the full response
    task = (
        db.query(DailyTask)
        .options(joinedload(DailyTask.topic).joinedload(Topic.subject),
                 joinedload(DailyTask.task_log))
        .filter(DailyTask.id == new_task.id)
        .first()
    )
    return task_service.build_task_response(task)

@router.get("", response_model=List[DailyTaskResponse])
def list_tasks(
    task_date: date,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    tasks = task_service.get_tasks_for_date(db, current_user.id, task_date)
    return [task_service.build_task_response(t) for t in tasks]

@router.patch("/{task_id}/log", response_model=TaskLogResponse)
def log_task_activity(
    task_id: int,
    data: TaskLogUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task_log = task_service.log_task(db, current_user.id, task_id, data)
    return task_log
