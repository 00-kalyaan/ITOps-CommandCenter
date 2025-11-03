from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship


class Asset(SQLModel, table=True):
id: Optional[int] = Field(default=None, primary_key=True)
hostname: str
ip: str
tags: Optional[str] = None


class Metric(SQLModel, table=True):
id: Optional[int] = Field(default=None, primary_key=True)
asset_id: int = Field(foreign_key="asset.id")
ts: datetime = Field(default_factory=datetime.utcnow)
cpu: float
ram: float
disk: float
ping_ms: Optional[float] = None


class Ticket(SQLModel, table=True):
id: Optional[int] = Field(default=None, primary_key=True)
asset_id: int = Field(foreign_key="asset.id")
severity: str
status: str = "OPEN" # OPEN | ACK | RESOLVED
summary: str
created_at: datetime = Field(default_factory=datetime.utcnow)
updated_at: datetime = Field(default_factory=datetime.utcnow)


class ActionLog(SQLModel, table=True):
id: Optional[int] = Field(default=None, primary_key=True)
ticket_id: Optional[int] = Field(default=None, foreign_key="ticket.id")
script: str
stdout: Optional[str] = None
stderr: Optional[str] = None
exit_code: Optional[int] = None
ts: datetime = Field(default_factory=datetime.utcnow)
