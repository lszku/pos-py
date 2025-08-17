"""Stock database models."""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from shared.models.enums import StockStatus

from ..core.database import Base


class StockEntry(Base):
    """Stock entry model for batch stock operations."""

    __tablename__ = "stock_entries"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    reference: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    notes: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    supplier: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    total_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    is_completed: Mapped[bool] = mapped_column(default=False)
    created_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    completed_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # Relationships
    stock_items: Mapped[list["Stock"]] = relationship("Stock", back_populates="stock_entry")
    user: Mapped["User"] = relationship("User")

    def __repr__(self) -> str:
        """String representation of StockEntry."""
        return f"<StockEntry(id={self.id}, reference='{self.reference}')>"


class Stock(Base):
    """Stock model for inventory management."""

    __tablename__ = "stock"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    stock_entry_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("stock_entries.id"), nullable=True
    )
    quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    cost_price: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    expiry_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    status: Mapped[StockStatus] = mapped_column(default=StockStatus.AVAILABLE)
    location: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    # Relationships
    product: Mapped["Product"] = relationship("Product")
    stock_entry: Mapped[Optional[StockEntry]] = relationship("StockEntry", back_populates="stock_items")

    def __repr__(self) -> str:
        """String representation of Stock."""
        return f"<Stock(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"
