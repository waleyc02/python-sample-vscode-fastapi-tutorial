# app/scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from .database import get_session
from .models import User
from .whatsapp import send_whatsapp_message, get_message

scheduler = BackgroundScheduler()

def send_daily_reminders():
    with get_session() as session:
        users = session.query(User).all()
        for user in users:
            msg = get_message("reminder", user.language)
            send_whatsapp_message(user.phone, msg)

def start_scheduler():
    scheduler.add_job(send_daily_reminders, 'interval', hours=24, next_run_time=datetime.now())
    scheduler.start()
