# app/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlmodel import Session
from zoneinfo import ZoneInfo
from .database import engine
from .models import User
from .whatsapp import send_whatsapp_message, get_message

scheduler = BackgroundScheduler(timezone=ZoneInfo("Europe/London"))

def send_daily_reminders():
    print("Running scheduled reminder job...")

    with Session(engine) as session:
        users = session.query(User).all()

        for user in users:
            lang = user.language or "en"
            msg = get_message("reminder", lang)
            send_whatsapp_message(user.phone, msg)

def start_scheduler():
    scheduler.add_job(
        send_daily_reminders,
        CronTrigger(hour=8, minute=0),  # 8:00 AM UK time
        id="daily_reminder",
        replace_existing=True
    )
    scheduler.start()