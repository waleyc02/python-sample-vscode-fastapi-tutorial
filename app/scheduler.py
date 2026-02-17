from apscheduler.schedulers.background import BackgroundScheduler
from app.whatsapp import send_whatsapp_message

scheduler = BackgroundScheduler()

def send_daily_reminder():
    send_whatsapp_message(
        "+447XXXXXXXXX",
        "Hello Ahmed 👋\nIt's time for your medication.\nReply 1 - Taken\n2 - Not yet"
    )

def start_scheduler():
    scheduler.add_job(send_daily_reminder, 'cron', hour=14, minute=0)
    scheduler.start()
