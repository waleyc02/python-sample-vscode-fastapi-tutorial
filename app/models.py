# app/models.py
from sqlmodel import SQLModel, Field
from datetime import datetime

class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    phone: str
    language: str = "en"  # Default language

class MedicationLog(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    phone: str
    response: str
    timestamp: datetime
