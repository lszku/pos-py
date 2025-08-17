"""Stock schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from shared.models.enums import StockStatus


class StockCreate(BaseModel):
    """Stock creation schema."""
    product_id: UUID
    stock_entry_id: Optional[UUID] = None
    quantity: int
    cost_price: Optional[Decimal] = None
    expiry_date: Optional[datetime] = None
    status: StockStatus = StockStatus.AVAILABLE
    location: Optional[str] = None


class StockUpdate(BaseModel):
    """Stock update schema."""
    quantity: Optional[int] = None
    cost_price: Optional[Decimal] = None
    expiry_date: Optional[datetime] = None
    status: Optional[StockStatus] = None
    location: Optional[str] = None


class StockResponse(BaseModel):
    """Stock response schema."""
    id: str
    product_id: str
    stock_entry_id: Optional[str] = None
    quantity: int
    cost_price: Optional[Decimal] = None
    expiry_date: Optional[datetime] = None
    status: StockStatus
    location: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class StockEntryCreate(BaseModel):
    """Stock entry creation schema."""
    reference: str
    notes: Optional[str] = None
    supplier: Optional[str] = None
    total_cost: Optional[Decimal] = None


class StockEntryResponse(BaseModel):
    """Stock entry response schema."""
    id: str
    reference: str
    notes: Optional[str] = None
    supplier: Optional[str] = None
    total_cost: Optional[Decimal] = None
    is_completed: bool
    created_by: str
    created_at: datetime
    completed_at: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""
        from_attributes = True
