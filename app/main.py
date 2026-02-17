from fastapi import FastAPI, Form
from app.whatsapp import send_whatsapp_message

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Tarastack running"}

@app.post("/webhook")
async def whatsapp_webhook(Body: str = Form(...), From: str = Form(...)):
    print(f"Message from {From}: {Body}")

    if Body.strip() == "1":
        reply = "Great 👍 I've logged this."
    elif Body.strip() == "2":
        reply = "No problem. I’ll remind you again in 30 minutes."
    else:
        reply = "Please reply with 1 (Taken) or 2 (Not yet)."

    send_whatsapp_message(From.replace("whatsapp:", ""), reply)

    return {"status": "ok"}
