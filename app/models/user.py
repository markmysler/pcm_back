from sqlalchemy import Column, String, Boolean, Enum, Integer, ForeignKey
from app.core.database import Base
from app.enums.roles import UserRole


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    username=Column(String, index=True)
    email = Column(String, unique=True, index=True)
    is_verified = Column(Boolean, default=False)
    avatar = Column(String, nullable=True)
    organization = Column(Integer, ForeignKey('organizations.id'), nullable=True)  # Foreign key column
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)