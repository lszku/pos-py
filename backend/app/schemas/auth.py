"""Authentication schemas."""

from typing import Optional

from pydantic import BaseModel, EmailStr

from shared.models.enums import UserRole


class Token(BaseModel):
    """Token response schema."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token data schema."""
    user_id: Optional[str] = None
    email: Optional[str] = None
    role: Optional[str] = None


class UserCreate(BaseModel):
    """User creation schema."""
    email: EmailStr
    password: str
    full_name: str
    role: UserRole = UserRole.CASHIER


class UserLogin(BaseModel):
    """User login schema."""
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    """User response schema."""
    id: str
    email: str
    full_name: Optional[str] = None
    role: UserRole
    is_active: bool

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class GoogleAuthRequest(BaseModel):
    """Google OAuth request schema."""
    id_token: str
