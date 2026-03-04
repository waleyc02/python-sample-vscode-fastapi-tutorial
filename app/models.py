# app/models.py
from sqlmodel import SQLModel, Field
from datetime import datetime, time
from typing import Optional

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    phone: str
    language: str = "en"
    reminder_time: time = time(8, 0)  # default 08:00

class MedicationLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    phone: str
    response: str
    timestamp: datetime
    message_sid: Optional[str] = None
    delivery_status: Optional[str] = None


class ReminderLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    phone: str
    sent_at: datetime