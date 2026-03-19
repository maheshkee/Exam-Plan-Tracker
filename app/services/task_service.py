from datetime import date
from typing import List
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.daily_task import DailyTask
from app.models.task_log import TaskLog
from app.models.topic import Topic
from app.models.user_exam import UserExam
from app.schemas.task import DailyTaskCreate, TaskLogUpdate

def get_user_enrollment(db: Session, user_id: int) -> UserExam:
    """Get enrollment or raise 404."""
    from app.services.exam_service import get_active_enrollment

    return get_active_enrollment(db, user_id)

def create_daily_task(db: Session, user_id: int, data: DailyTaskCreate) -> DailyTask:
    enrollment = get_user_enrollment(db, user_id)

    # Verify topic exists and join with subject to check exam_id
    topic = (
        db.query(Topic)
        .join(Topic.subject)
        .filter(Topic.id == data.topic_id)
        .first()
    )
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    # Check topic belongs to enrolled exam
    if topic.subject.exam_id != enrollment.exam_id:
        raise HTTPException(
            status_code=400,
            detail="Topic does not belong to your enrolled exam"
        )

    task = DailyTask(
        user_exam_id=enrollment.id,
        topic_id=data.topic_id,
        task_date=data.task_date,
        planned_hours=data.planned_hours,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def get_tasks_for_date(db: Session, user_id: int, task_date: date) -> List[DailyTask]:
    enrollment = get_user_enrollment(db, user_id)
    return (
        db.query(DailyTask)
        .options(joinedload(DailyTask.topic).joinedload(Topic.subject),
                 joinedload(DailyTask.task_log))
        .filter(
            DailyTask.user_exam_id == enrollment.id,
            DailyTask.task_date == task_date,
        )
        .all()
    )

def log_task(db: Session, user_id: int, task_id: int, data: TaskLogUpdate) -> TaskLog:
    enrollment = get_user_enrollment(db, user_id)

    task = db.query(DailyTask).filter(
        DailyTask.id == task_id,
        DailyTask.user_exam_id == enrollment.id,
    ).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Create or update TaskLog
    task_log = db.query(TaskLog).filter(TaskLog.daily_task_id == task_id).first()
    if task_log:
        task_log.status = data.status
        if data.actual_hours is not None:
            task_log.actual_hours = data.actual_hours
        else:
             # If status is updated but actual_hours not provided, 
             # and it was previously set, we keep it. 
             # If it was None, we might want to default it to planned_hours.
             if task_log.actual_hours is None:
                 task_log.actual_hours = task.planned_hours
    else:
        task_log = TaskLog(
            daily_task_id=task_id,
            status=data.status,
            actual_hours=data.actual_hours if data.actual_hours is not None
                        else task.planned_hours,
        )
        db.add(task_log)

    db.commit()
    db.refresh(task_log)
    return task_log

def build_task_response(task: DailyTask) -> dict:
    """Build response dict with denormalized topic/subject names."""
    return {
        "id": task.id,
        "topic_id": task.topic_id,
        "topic_name": task.topic.name,
        "subject_name": task.topic.subject.name,
        "task_date": task.task_date,
        "planned_hours": task.planned_hours,
        "task_log": task.task_log,
    }
