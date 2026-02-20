from fastapi import FastAPI, Form, Depends
from sqlmodel import Session
from datetime import datetime
from .models import User, MedicationLog
from .database import get_session, init_db
from .whatsapp import send_whatsapp_message, get_message
from .scheduler import start_scheduler

app = FastAPI()

@app.on_event("startup")
def on_startup():
    init_db()
    start_scheduler()

@app.post("/webhook")
async def whatsapp_webhook(
    Body: str = Form(...),
    From: str = Form(...),
    session: Session = Depends(get_session)
):
    phone = From.replace("whatsapp:", "") if From.startswith("whatsapp:") else From
    msg = Body.strip()

    user = session.query(User).filter(User.phone == phone).first()
    if not user:
        user = User(phone=phone)
        session.add(user)
        session.commit()

    lang = user.language or "en"
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
        reminder_text = get_message("reminder", lang)
        send_whatsapp_message(phone, reminder_text)
        return "OK"