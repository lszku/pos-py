"""Sale schemas."""

from datetime import datetime
from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from shared.models.enums import SaleStatus


class SaleCreate(BaseModel):
    """Sale creation schema."""
    items: list
    payment_method: str
    total_amount: str
    reference: Optional[str] = None
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    discount_amount: Decimal = Decimal("0")
    tax_amount: Decimal = Decimal("0")
    final_amount: Optional[Decimal] = None
    status: SaleStatus = SaleStatus.PENDING
    notes: Optional[str] = None


class SaleUpdate(BaseModel):
    """Sale update schema."""
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    total_amount: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    tax_amount: Optional[Decimal] = None
    final_amount: Optional[Decimal] = None
    status: Optional[SaleStatus] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class SaleResponse(BaseModel):
    """Sale response schema."""
    id: str
    reference: str
    customer_name: Optional[str] = None
    customer_email: Optional[str] = None
    total_amount: Decimal
    discount_amount: Decimal
    tax_amount: Decimal
    final_amount: Decimal
    status: SaleStatus
    payment_method: Optional[str] = None
    notes: Optional[str] = None
    created_by: str
    created_at: datetime
    completed_at: Optional[datetime] = None
    items: Optional[list] = None

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class SaleItemCreate(BaseModel):
    """Sale item creation schema."""
    sale_id: UUID
    product_id: UUID
    quantity: int
    unit_price: Decimal
    discount_amount: Decimal = Decimal("0")
    total_amount: Decimal


class SaleItemResponse(BaseModel):
    """Sale item response schema."""
    id: str
    sale_id: str
    product_id: str
    quantity: int
    unit_price: Decimal
    discount_amount: Decimal
    total_amount: Decimal
    created_at: datetime

    class Config:
        """Pydantic configuration."""
        from_attributes = True
