from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone: str

class MedicationLog(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    phone: str
    response: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
