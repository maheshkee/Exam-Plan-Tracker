import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.config import settings

def send_reminder_email(to_email: str, user_name: str) -> bool:
    """
    Send a study reminder email.
    Returns True if sent, False if failed (so caller can decide to log or not).
    """
    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = "📚 Don't forget your study session today!"
        msg["From"] = settings.EMAIL_USERNAME
        msg["To"] = to_email

        body = f"""
Hi there,

This is a reminder that you haven't logged any study activity today.

Log in to Exam Plan Tracker and mark your progress.

Stay consistent — every day counts!

— Exam Plan Tracker
        """

        msg.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT) as server:
            server.starttls()
            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            server.sendmail(settings.EMAIL_USERNAME, to_email, msg.as_string())

        return True

    except Exception as e:
        print(f"[Email Error] Failed to send to {to_email}: {e}")
        return False
