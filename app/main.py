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

@app.post("/status")
async def message_status(
    MessageSid: str = Form(...),
    MessageStatus: str = Form(...),
    session: Session = Depends(get_session)
):
    log = session.query(MedicationLog).filter(
        MedicationLog.message_sid == MessageSid
    ).first()

    if log:
        log.delivery_status = MessageStatus
        session.add(log)
        session.commit()

    print(f"Message {MessageSid} status updated to {MessageStatus}")
    return "OK"

def detect_language(message: str):
    french_keywords = ["bonjour", "oui", "non"]
    if any(word in message.lower() for word in french_keywords):
        return "fr"
    return "en"

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
        detected_lang = detect_language(msg)
        user = User(phone=phone, language=detected_lang)
        session.add(user)
        session.commit()

    lang = user.language or "en"
    timestamp = datetime.utcnow()
    msg_clean = msg.strip().lower()

    if msg_clean in ["1", "YES", "yes"]:
        message_sid = send_whatsapp_message(phone, get_message("yes_response", lang))

        log = MedicationLog(
            phone=phone,
            response="YES",
            timestamp=timestamp,
            message_sid=message_sid
        )
        session.add(log)
        session.commit()
        return "OK"


    elif msg_clean in ["2", "NO", "no"]:
        message_sid = send_whatsapp_message(phone, get_message("no_response", lang))

        log = MedicationLog(
            phone=phone,
            response="NO",
            timestamp=timestamp,
            message_sid=message_sid
        )
        session.add(log)
        session.commit()
        return "OK"

    else:
        reminder_text = get_message("reminder", lang)
        message_sid = send_whatsapp_message(phone, reminder_text)

        log = MedicationLog(
            phone=phone,
            response="REMINDER_SENT",
            timestamp=timestamp,
            message_sid=message_sid
        )
        session.add(log)
        session.commit()
        return "OK"