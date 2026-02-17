# app/main.py
from fastapi import FastAPI, Form
from datetime import datetime
from .models import User, MedicationLog
from .database import get_session, init_db
from .whatsapp import send_whatsapp_message, get_message
from .scheduler import start_scheduler

# -------------------------------
# INIT
# -------------------------------
init_db()
start_scheduler()
app = FastAPI()

@app.post("/webhook")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    phone = From.replace("whatsapp:", "") if From.startswith("whatsapp:") else From
    msg = Body.strip()

    with get_session() as session:
        user = session.query(User).filter(User.phone == phone).first()
        if not user:
            user = User(phone=phone)
            session.add(user)
            session.commit()

        # Default language for new users
        lang = user.language or "en"

        # YES/NO responses
        timestamp = datetime.utcnow()
        if msg in ["1", "YES", "yes"]:
            log = MedicationLog(phone=phone, response="YES", timestamp=timestamp)
            session.add(log)
            session.commit()
            send_whatsapp_message(phone, get_message("yes_response", lang))
            return "OK"

        elif msg in ["2", "NO", "no"]:
            log = MedicationLog(phone=phone, response="NO", timestamp=timestamp)
            session.add(log)
            session.commit()
            send_whatsapp_message(phone, get_message("no_response", lang))
            return "OK"

        else:
            # Send reminder
            reminder_text = get_message("reminder", lang)
            send_whatsapp_message(phone, reminder_text)
            return "OK"
