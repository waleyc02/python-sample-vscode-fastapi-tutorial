from fastapi import FastAPI, Form
from sqlmodel import Session, select
from app.database import engine, create_db
from app.models import User, MedicationLog

app = FastAPI()

create_db()

@app.post("/webhook")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):

    phone = From.replace("whatsapp:", "")

    with Session(engine) as session:

        # Ensure user exists
        statement = select(User).where(User.phone == phone)
        user = session.exec(statement).first()

        if not user:
            user = User(phone=phone)
            session.add(user)
            session.commit()

        # Handle responses
        if Body.strip() == "1":
            log = MedicationLog(phone=phone, response="YES")
            session.add(log)
            session.commit()
            return "Logged as taken. Great job!"

        elif Body.strip() == "2":
            log = MedicationLog(phone=phone, response="NO")
            session.add(log)
            session.commit()
            return "Noted. Please take it as soon as possible."

        else:
            return """Hello!
Reminder:
- Take Paracetamol
- Take Blood Tonic

Reply:
1 - Yes
2 - No"""
