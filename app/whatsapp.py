# app/whatsapp.py
from twilio.rest import Client
from .config import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_NUMBER, DEFAULT_LANGUAGE, SUPPORTED_LANGUAGES

client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# -------------------------------
# Multilingual messages
# -------------------------------
MESSAGES = {
    "reminder": {
        "en": (
            "Hello!\n"
            "Reminder for your medication today:\n"
            "- Take Repondixyl\n"
            "- Take Blood Tonic\n\n"
            "Reply:\n"
            "1 - Yes\n"
            "2 - No"
        ),
        "es": (
            "¡Hola!\n"
            "Recordatorio de tu medicación de hoy:\n"
            "- Tomar Repondixyl\n"
            "- Tomar Tónico de Sangre\n\n"
            "Responde:\n"
            "1 - Sí\n"
            "2 - No"
        ),
        "fr": (
            "Bonjour!\n"
            "Rappel pour votre médicament d'aujourd'hui:\n"
            "- Prendre Repondixyl\n"
            "- Prendre Tonic Sanguin\n\n"
            "Répondez:\n"
            "1 - Oui\n"
            "2 - Non"
        )
    },
    "yes_response": {
        "en": "✅ Logged as taken. Great job!",
        "es": "✅ Registrado como tomado. ¡Buen trabajo!",
        "fr": "✅ Enregistré comme pris. Bravo!"
    },
    "no_response": {
        "en": "⚠️ Noted. Please take it as soon as possible.",
        "es": "⚠️ Notado. Por favor tómalo lo antes posible.",
        "fr": "⚠️ Noté. Veuillez le prendre dès que possible."
    }
}

def get_message(key: str, lang: str = DEFAULT_LANGUAGE) -> str:
    """Get multilingual message, fallback to default language"""
    if lang not in SUPPORTED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
    return MESSAGES[key][lang]

def send_whatsapp_message(to: str, message: str):
    """Send WhatsApp message via Twilio with delivery tracking"""

    if not to.startswith("whatsapp:"):
        to = f"whatsapp:{to}"

    msg = client.messages.create(
        body=message,
        from_=TWILIO_WHATSAPP_NUMBER,
        to=to,
        status_callback="https://tarastack-api.onrender.com/status"
    )

    return msg.sid  # 🔥 Return SID
