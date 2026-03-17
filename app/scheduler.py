from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = BackgroundScheduler()

def start_scheduler():
    from app.services.notification_service import send_reminders_for_all_users

    # Run every day at 8:00 PM
    scheduler.add_job(
        send_reminders_for_all_users,
        trigger=CronTrigger(hour=20, minute=0),
        id="daily_reminder",
        replace_existing=True,
    )
    scheduler.start()
    print("[Scheduler] Daily reminder job scheduled at 20:00")

def stop_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        print("[Scheduler] Stopped")
