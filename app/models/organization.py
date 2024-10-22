from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from app.core.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    logo = Column(String, nullable=True)
