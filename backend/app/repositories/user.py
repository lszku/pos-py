"""User repository with authentication methods."""

from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.user import User
from .base import BaseRepository


class UserRepository(BaseRepository[User]):
    """User repository with authentication methods."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize user repository."""
        super().__init__(User, session)

    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        stmt = select(User).where(User.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_google_id(self, google_id: str) -> Optional[User]:
        """Get user by Google ID."""
        stmt = select(User).where(User.google_id == google_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create_user(self, email: str, hashed_password: Optional[str] = None,
                         full_name: Optional[str] = None, google_id: Optional[str] = None,
                         role: Optional[str] = None) -> User:
        """Create new user."""
        return await self.create(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            google_id=google_id,
            role=role
        )
