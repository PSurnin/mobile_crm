from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict

class LeadStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    closed = "closed"

class LeadCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr

class Lead(BaseModel):
    id: int
    name: str
    phone: str
    email: EmailStr
    status: LeadStatus = LeadStatus.new

    model_config = ConfigDict(from_attributes=True)

class LeadStatusUpdate(BaseModel):
    status: LeadStatus