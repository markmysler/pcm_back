import enum
from sqlalchemy import Column, Enum as SqlEnum

class UserRole(enum.Enum):
    USER = "user"
    ORG_ADMIN = "org_admin"
    MANAGER = "manager"
    PERI_ADMIN = "peri_admin"
    SUPER_ADMIN = "super_admin"