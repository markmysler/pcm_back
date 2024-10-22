from typing import Optional
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from app.enums.roles import UserRole

class OrgCreate(BaseModel):
    name: str
    logo:Optional[str] = None

class OrgOut(BaseModel):
    id: str
    name: str
    logo:Optional[str] = None
    
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True,
        alias_generator=lambda s: ''.join([s[0].lower()] + [c if c.islower() else f"_{c.lower()}" for c in s[1:]])
    )
