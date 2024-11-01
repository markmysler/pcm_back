from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from app.enums.roles import UserRole
from typing import Optional

class UserCreate(BaseModel):
    name: str
    surname: str
    username: str
    email: EmailStr
    password: str
    organization: Optional[int] = None
    role: Optional[UserRole] = None

    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(c.islower() for c in v):
            raise ValueError("Password must contain at least one lowercase letter")
        if not any(c.isupper() for c in v):
            raise ValueError("Password must contain at least one uppercase letter")
        if not any(c.isdigit() for c in v):
            raise ValueError("Password must contain at least one number")
        return v

class UserOut(BaseModel):
    id: str
    name: str
    surname: str
    username: str
    email: EmailStr
    is_verified: bool
    organization: int
    role: UserRole

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=lambda s: ''.join([s[0].lower()] + [c if c.islower() else f"_{c.lower()}" for c in s[1:]])
    )
    
    
class VerificationRequest(BaseModel):
    user_id: str
    verification_code: str
    
class TokenRequest(BaseModel):
    username: str
    password: str