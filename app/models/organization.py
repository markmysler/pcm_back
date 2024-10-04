from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from app.core.database import Base


class Organization(Base):
    __tablename__ = "organizations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    manager = Column(String, ForeignKey('users.id'), nullable=False)  # Foreign key column
    logo = Column(String, nullable=True)
