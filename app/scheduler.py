# app/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlmodel import Session
from zoneinfo import ZoneInfo
from .database import engine
from .models import User, ReminderLog
from .whatsapp import send_whatsapp_message, get_message
from datetime import datetime, date


scheduler = BackgroundScheduler(timezone=ZoneInfo("Europe/London"))


def send_daily_reminders():
    today = date.today()
    now = datetime.now()

    with Session(engine) as session:
        users = session.query(User).all()

        for user in users:
            reminder_datetime = datetime.combine(today, user.reminder_time)

            if now < reminder_datetime:
                continue

            # Check if reminder already sent today
            existing = session.query(ReminderLog).filter(
                ReminderLog.phone == user.phone,
                ReminderLog.sent_at >= datetime.combine(today, datetime.min.time())
            ).first()

            if existing:
                continue  # Skip duplicate

            lang = user.language or "en"
            msg = get_message("reminder", lang)

            send_whatsapp_message(user.phone, msg)

            # Log reminder
            reminder_log = ReminderLog(
                phone=user.phone,
                sent_at=datetime.utcnow()
            )
            session.add(reminder_log)
            session.commit()

def start_scheduler():
    scheduler.add_job(
        send_daily_reminders,
        trigger="interval",
        minutes=5,
        id="reminder_check",
        replace_existing=True
    )
    scheduler.start()