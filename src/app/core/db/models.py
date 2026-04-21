from sqlalchemy import Column, Integer, String
from app.core.db.database import Base

class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    email = Column(String, nullable=False)
    status = Column(String, default="new", nullable=False)
