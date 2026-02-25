# app/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from sqlmodel import Session
from .database import engine
from .models import User
from .whatsapp import send_whatsapp_message, get_message

scheduler = BackgroundScheduler()

def send_daily_reminders():
    print("Running daily reminder job...")

    with Session(engine) as session:
        users = session.query(User).all()

        for user in users:
            lang = user.language or "en"
            msg = get_message("reminder", lang)
            send_whatsapp_message(user.phone, msg)

def start_scheduler():
    scheduler.add_job(
        send_daily_reminders,
        trigger="interval",
        hours=24,
        next_run_time=datetime.now()  # runs immediately on startup
    )
    scheduler.start()