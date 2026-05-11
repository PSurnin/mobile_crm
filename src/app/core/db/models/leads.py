from datetime import datetime
from sqlalchemy import String, Enum as SAEnum, DateTime, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from src.app.core.db.database import Base
from src.app.core.schemas.leads import LeadStatus

class LeadModel(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    status: Mapped[LeadStatus] = mapped_column(
        SAEnum(LeadStatus), default=LeadStatus.new
    )
    assigned_to: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    telegram_id: Mapped[int | None] = mapped_column()


# TODO: public id - 
# public_id: Mapped[str] = mapped_column(
#    String(36), default=lambda: str(uuid.uuid4()), unique=True
#)