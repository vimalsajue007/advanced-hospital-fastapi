from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    specialization = Column(String)
    email = Column(String, unique=True)
    is_active = Column(Boolean, default=True)