import uuid
from datetime import datetime
from decimal import Decimal
from sqlalchemy import String, Enum as SAEnum, DateTime, func, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from src.app.core.db.database import Base
from src.app.core.schemas.leads import LeadStatus

class LeadModel(Base):
    __tablename__ = "leads"

    id: Mapped[int] = mapped_column(primary_key=True)
    public_id: Mapped[str] = mapped_column(
    String(36), default=lambda: str(uuid.uuid4()), unique=True
    )
    name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(255))
    status: Mapped[LeadStatus] = mapped_column(
        SAEnum(LeadStatus), default=LeadStatus.new
    )
    assigned_to: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    telegram_id: Mapped[int | None]
    contacted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    amount: Mapped[Decimal | None] = mapped_column(Numeric(12, 2))
    lost_reason: Mapped[str | None] = mapped_column(String(255))
