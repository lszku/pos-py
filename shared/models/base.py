"""Base model for shared entities."""

from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel as PydanticBaseModel, Field


class BaseModel(PydanticBaseModel):
    """Base model with common fields and configuration."""

    class Config:
        """Pydantic configuration."""
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }


class TimestampedModel(BaseModel):
    """Base model with timestamp fields."""

    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class PaginatedResponse(BaseModel):
    """Generic paginated response model."""

    items: list[Any] = Field(default_factory=list)
    total: int = Field(default=0)
    page: int = Field(default=1)
    size: int = Field(default=20)
    pages: int = Field(default=0)

    def __init__(self, **data: Any) -> None:
        """Initialize paginated response."""
        super().__init__(**data)
        if self.total > 0 and self.size > 0:
            self.pages = (self.total + self.size - 1) // self.size 