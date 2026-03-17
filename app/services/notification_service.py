from datetime import date, datetime
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user_exam import UserExam
from app.models.daily_task import DailyTask
from app.models.task_log import TaskLog
from app.models.notification_log import NotificationLog
from app.models.user import User
from app.utils.email import send_reminder_email

def has_activity_today(db: Session, user_exam_id: int) -> bool:
    """Returns True if user has any TaskLog entry updated today."""
    today = date.today()
    result = (
        db.query(TaskLog)
        .join(DailyTask, DailyTask.id == TaskLog.daily_task_id)
        .filter(
            DailyTask.user_exam_id == user_exam_id,
            DailyTask.task_date == today,
        )
        .first()
    )
    return result is not None

def already_notified_today(db: Session, user_exam_id: int) -> bool:
    """Returns True if a reminder was already sent today."""
    today = date.today()
    result = db.query(NotificationLog).filter(
        NotificationLog.user_exam_id == user_exam_id,
        NotificationLog.notification_type == "REMINDER",
    ).filter(
        NotificationLog.sent_at >= datetime.combine(today, datetime.min.time())
    ).first()
    return result is not None

def send_reminders_for_all_users():
    """
    Called by scheduler. Checks all enrolled users.
    Sends reminder if:
      - User has no activity today
      - No reminder sent today yet
    """
    db = SessionLocal()
    try:
        enrollments = db.query(UserExam).all()
        for enrollment in enrollments:
            if already_notified_today(db, enrollment.id):
                continue
            if has_activity_today(db, enrollment.id):
                continue

            user = db.query(User).filter(User.id == enrollment.user_id).first()
            if not user:
                continue

            sent = send_reminder_email(user.email, user.email)

            if sent:
                log = NotificationLog(
                    user_exam_id=enrollment.id,
                    notification_type="REMINDER",
                )
                db.add(log)
                db.commit()
                print(f"[Notification] Reminder sent to {user.email}")
            else:
                print(f"[Notification] Failed to send to {user.email}")
    finally:
        db.close()
