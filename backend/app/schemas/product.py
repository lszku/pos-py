"""Product schemas."""

from decimal import Decimal
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from shared.models.enums import ProductCategory


class ProductCreate(BaseModel):
    """Product creation schema."""
    name: str
    description: Optional[str] = None
    sku: str
    category: ProductCategory
    price: Decimal
    cost_price: Optional[Decimal] = None
    image_url: Optional[str] = None


class ProductUpdate(BaseModel):
    """Product update schema."""
    name: Optional[str] = None
    description: Optional[str] = None
    sku: Optional[str] = None
    category: Optional[ProductCategory] = None
    price: Optional[Decimal] = None
    cost_price: Optional[Decimal] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class ProductResponse(BaseModel):
    """Product response schema."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    description: Optional[str] = None
    sku: str
    category: ProductCategory
    price: Decimal
    cost_price: Optional[Decimal] = None
    image_url: Optional[str] = None
    is_active: bool
