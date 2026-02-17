# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load .env file

# Twilio
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WHATSAPP_NUMBER")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./medication.db")

# Supported languages
SUPPORTED_LANGUAGES = ["en", "es", "fr"]  # English, Spanish, French
DEFAULT_LANGUAGE = "en"
