"""Stock and StockEntry repositories."""

from typing import Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.enums import StockStatus

from ..models.stock import Stock, StockEntry
from .base import BaseRepository


class StockRepository(BaseRepository[Stock]):
    """Stock repository with inventory management methods."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize stock repository."""
        super().__init__(Stock, session)

    async def get_by_product(self, product_id: UUID) -> list[Stock]:
        """Get stock items by product ID."""
        stmt = select(Stock).where(Stock.product_id == product_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_available_stock(self, product_id: UUID) -> int:
        """Get total available stock for a product."""
        stmt = select(func.sum(Stock.quantity)).where(
            Stock.product_id == product_id,
            Stock.status == StockStatus.AVAILABLE
        )
        result = await self.session.execute(stmt)
        return result.scalar() or 0

    async def get_low_stock_products(self, threshold: int = 10) -> list[Stock]:
        """Get products with low stock."""
        stmt = (
            select(Stock)
            .where(Stock.quantity <= threshold)
            .where(Stock.status == StockStatus.AVAILABLE)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update_stock_quantity(self, stock_id: UUID, quantity: int) -> Optional[Stock]:
        """Update stock quantity."""
        return await self.update(stock_id, quantity=quantity)


class StockEntryRepository(BaseRepository[StockEntry]):
    """Stock entry repository for batch operations."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize stock entry repository."""
        super().__init__(StockEntry, session)

    async def get_incomplete_entries(self, user_id: UUID) -> list[StockEntry]:
        """Get incomplete stock entries for a user."""
        stmt = (
            select(StockEntry)
            .where(StockEntry.created_by == user_id)
            .where(StockEntry.is_completed == False)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def complete_entry(self, entry_id: UUID) -> Optional[StockEntry]:
        """Mark stock entry as completed."""
        from datetime import datetime
        return await self.update(
            entry_id,
            is_completed=True,
            completed_at=datetime.utcnow()
        )
