from datetime import date
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from app.models.user_exam import UserExam
from app.models.daily_task import DailyTask
from app.models.task_log import TaskLog
from app.models.progress_snapshot import ProgressSnapshot
from app.models.exam import Exam
from app.models.topic import Topic


def get_dashboard_data(db: Session, user_id: int) -> dict:
    from app.services.task_service import get_user_enrollment
    from app.services.exam_service import get_exam_with_syllabus, calculate_total_syllabus_hours

    enrollment = get_user_enrollment(db, user_id)
    exam = get_exam_with_syllabus(db, enrollment.exam_id)

    today = date.today()
    days_remaining = (enrollment.exam_date - today).days
    days_elapsed = (today - enrollment.created_at.date()).days
    days_elapsed = max(days_elapsed, 1)  # avoid division by zero

    # Syllabus totals
    total_topics = sum(len(s.topics) for s in exam.subjects)
    total_syllabus_hours = calculate_total_syllabus_hours(exam)

    # Completed topics: distinct topic_ids where TaskLog status = COMPLETED
    completed_topic_ids = (
        db.query(DailyTask.topic_id)
        .join(TaskLog, TaskLog.daily_task_id == DailyTask.id)
        .filter(
            DailyTask.user_exam_id == enrollment.id,
            TaskLog.status == "COMPLETED"
        )
        .distinct()
        .all()
    )
    topics_completed = len(completed_topic_ids)
    completion_pct = round((topics_completed / total_topics) * 100, 1) if total_topics > 0 else 0.0

    # Hours studied (sum of actual_hours from COMPLETED logs)
    hours_studied = db.query(func.sum(TaskLog.actual_hours))\
        .join(DailyTask, DailyTask.id == TaskLog.daily_task_id)\
        .filter(
            DailyTask.user_exam_id == enrollment.id,
            TaskLog.status == "COMPLETED"
        ).scalar() or 0.0

    actual_hours_per_day = round(hours_studied / days_elapsed, 2)
    required_per_day = round(total_syllabus_hours / days_remaining, 2) if days_remaining > 0 else 0.0

    # Pace status
    if actual_hours_per_day >= required_per_day * 1.1:
        pace_status = "AHEAD"
    elif actual_hours_per_day >= required_per_day * 0.85:
        pace_status = "ON_TRACK"
    else:
        pace_status = "BEHIND"

    # Today's tasks
    today_tasks = db.query(DailyTask)\
        .options(joinedload(DailyTask.task_log))\
        .filter(
            DailyTask.user_exam_id == enrollment.id,
            DailyTask.task_date == today,
        ).all()
    tasks_today = len(today_tasks)
    tasks_completed_today = sum(
        1 for t in today_tasks
        if t.task_log and t.task_log.status == "COMPLETED"
    )

    return {
        "exam_name": exam.name,
        "exam_date": enrollment.exam_date,
        "days_remaining": days_remaining,
        "total_topics": total_topics,
        "topics_completed": topics_completed,
        "completion_percentage": completion_pct,
        "total_syllabus_hours": total_syllabus_hours,
        "hours_studied": hours_studied,
        "required_hours_per_day": required_per_day,
        "actual_hours_per_day": actual_hours_per_day,
        "pace_status": pace_status,
        "tasks_today": tasks_today,
        "tasks_completed_today": tasks_completed_today,
    }


def generate_end_of_day(db: Session, user_id: int, target_date: date) -> dict:
    from app.services.task_service import get_user_enrollment
    from app.services.exam_service import get_exam_with_syllabus, calculate_total_syllabus_hours

    enrollment = get_user_enrollment(db, user_id)

    tasks = db.query(DailyTask)\
        .options(joinedload(DailyTask.task_log))\
        .filter(
            DailyTask.user_exam_id == enrollment.id,
            DailyTask.task_date == target_date,
        ).all()

    tasks_planned = len(tasks)
    tasks_completed = sum(1 for t in tasks if t.task_log and t.task_log.status == "COMPLETED")
    tasks_skipped = sum(1 for t in tasks if t.task_log and t.task_log.status == "SKIPPED")
    tasks_pending = sum(1 for t in tasks if not t.task_log)
    hours_planned = sum(t.planned_hours for t in tasks)
    hours_completed = sum(
        t.task_log.actual_hours for t in tasks
        if t.task_log and t.task_log.status == "COMPLETED" and t.task_log.actual_hours
    )

    if tasks_planned == 0:
        day_status = "MISSED"
    elif tasks_completed == tasks_planned:
        day_status = "COMPLETED"
    elif tasks_completed > 0:
        day_status = "PARTIAL"
    else:
        day_status = "MISSED"

    # Calculate pace for snapshot
    exam = get_exam_with_syllabus(db, enrollment.exam_id)
    total_syllabus_hours = calculate_total_syllabus_hours(exam)
    days_remaining = (enrollment.exam_date - target_date).days
    required_per_day = round(total_syllabus_hours / days_remaining, 2) if days_remaining > 0 else 0.0
    daily_avg = hours_completed
    if daily_avg >= required_per_day * 1.1:
        pace_status = "AHEAD"
    elif daily_avg >= required_per_day * 0.5:
        pace_status = "ON_TRACK"
    else:
        pace_status = "BEHIND"

    # Count completed topics as of today
    completed_topics = db.query(DailyTask.topic_id)\
        .join(TaskLog, TaskLog.daily_task_id == DailyTask.id)\
        .filter(
            DailyTask.user_exam_id == enrollment.id,
            TaskLog.status == "COMPLETED"
        ).distinct().count()

    total_hours_done = db.query(func.sum(TaskLog.actual_hours))\
        .join(DailyTask, DailyTask.id == TaskLog.daily_task_id)\
        .filter(
            DailyTask.user_exam_id == enrollment.id,
            TaskLog.status == "COMPLETED"
        ).scalar() or 0.0

    # Upsert ProgressSnapshot
    snapshot = db.query(ProgressSnapshot).filter(
        ProgressSnapshot.user_exam_id == enrollment.id,
        ProgressSnapshot.snapshot_date == target_date,
    ).first()

    if snapshot:
        snapshot.topics_completed = completed_topics
        snapshot.hours_completed = total_hours_done
        snapshot.pace_status = pace_status
    else:
        snapshot = ProgressSnapshot(
            user_exam_id=enrollment.id,
            snapshot_date=target_date,
            topics_completed=completed_topics,
            hours_completed=total_hours_done,
            pace_status=pace_status,
        )
        db.add(snapshot)

    db.commit()

    return {
        "snapshot_date": target_date,
        "tasks_planned": tasks_planned,
        "tasks_completed": tasks_completed,
        "tasks_skipped": tasks_skipped,
        "tasks_pending": tasks_pending,
        "hours_planned": hours_planned,
        "hours_completed": hours_completed,
        "day_status": day_status,
        "pace_status": pace_status,
    }


def get_progress_history(db: Session, user_id: int) -> List[ProgressSnapshot]:
    from app.services.task_service import get_user_enrollment
    enrollment = get_user_enrollment(db, user_id)
    return db.query(ProgressSnapshot)\
        .filter(ProgressSnapshot.user_exam_id == enrollment.id)\
        .order_by(ProgressSnapshot.snapshot_date.desc())\
        .all()
