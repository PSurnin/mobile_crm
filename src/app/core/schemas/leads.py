from datetime import datetime
from decimal import Decimal
from enum import Enum
from pydantic import AwareDatetime, BaseModel, EmailStr, ConfigDict

class LeadStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    won = "won"
    lost = "lost"

class LeadCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr

class Lead(BaseModel):
    public_id: str
    name: str
    phone: str
    email: EmailStr
    status: LeadStatus = LeadStatus.new
    contacted_at: AwareDatetime | None = None
    closed_at: AwareDatetime | None = None
    amount: Decimal | None = None
    lost_reason: str | None = None

    model_config = ConfigDict(from_attributes=True)

class LeadStatusUpdate(BaseModel):
    status: LeadStatus
    amount: Decimal | None = None
    lost_reason: str | None = None

class BotLeadCreate(LeadCreate):
    invite_token: str
    telegram_id: int
