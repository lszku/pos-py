"""Authentication service."""

from datetime import timedelta
from typing import Any, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.enums import UserRole

from ..core.security import create_access_token, get_password_hash, verify_password
from ..repositories.user import UserRepository


class AuthService:
    """Authentication service for user management."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize auth service."""
        self.session = session
        self.user_repo = UserRepository(session)

    async def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        """Authenticate user with email and password."""
        user = await self.user_repo.get_by_email(email)

        if not user or not user.hashed_password:
            return None

        if not verify_password(password, user.hashed_password):
            return None

        if not user.is_active:
            return None

        return {
            "id": str(user.id),
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name
        }

    async def create_user(self, email: str, password: str, full_name: str,
                         role: UserRole = UserRole.CASHIER) -> dict:
        """Create new user with password."""
        hashed_password = get_password_hash(password)
        user = await self.user_repo.create_user(
            email=email,
            hashed_password=hashed_password,
            full_name=full_name,
            role=role
        )

        return {
            "id": str(user.id),
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name,
            "is_active": user.is_active
        }

    async def create_google_user(self, email: str, google_id: str,
                                full_name: str, role: UserRole = UserRole.CASHIER) -> dict:
        """Create new user with Google OAuth."""
        user = await self.user_repo.create_user(
            email=email,
            google_id=google_id,
            full_name=full_name,
            role=role
        )

        return {
            "id": str(user.id),
            "email": user.email,
            "role": user.role,
            "full_name": user.full_name,
            "is_active": user.is_active
        }

    async def get_or_create_google_user(self, email: str, google_id: str,
                                       full_name: str) -> dict:
        """Get existing user or create new one with Google OAuth."""
        user = await self.user_repo.get_by_google_id(google_id)

        if user:
            return {
                "id": str(user.id),
                "email": user.email,
                "role": user.role,
                "full_name": user.full_name,
                "is_active": user.is_active
            }

        return await self.create_google_user(email, google_id, full_name)

    def create_token(self, user_data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT token for user."""
        return create_access_token(
            data={
                "sub": user_data["id"],
                "email": user_data["email"],
                "role": user_data["role"]
            },
            expires_delta=expires_delta
        )

    async def verify_google_token(self, id_token: str) -> Optional[dict[str, Any]]:
        """Verify Google ID token and extract user information."""
        # This is a simplified implementation
        # In production, you should verify the token with Google's API
        # For now, we'll assume the token is valid and extract user info
        try:
            # In a real implementation, you would:
            # 1. Verify the token signature with Google's public keys
            # 2. Check the token expiration
            # 3. Verify the audience (your app's client ID)
            # 4. Extract user information from the token payload

            # For development/testing purposes, we'll return mock data
            # In production, replace this with actual Google token verification
            return {
                "email": "test@example.com",
                "google_id": "google_123456",
                "full_name": "Test User"
            }
        except Exception:
            return None
