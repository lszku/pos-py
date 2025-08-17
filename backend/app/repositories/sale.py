"""Sale repository."""

from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.enums import SaleStatus

from ..models.sale import Sale, SaleItem
from .base import BaseRepository


class SaleRepository(BaseRepository[Sale]):
    """Sale repository with sales management methods."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize sale repository."""
        super().__init__(Sale, session)

    async def get_by_user(self, user_id: UUID, skip: int = 0, limit: int = 20) -> list[Sale]:
        """Get sales by user ID."""
        stmt = (
            select(Sale)
            .where(Sale.created_by == user_id)
            .order_by(Sale.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_status(self, status: SaleStatus, skip: int = 0, limit: int = 20) -> list[Sale]:
        """Get sales by status."""
        stmt = (
            select(Sale)
            .where(Sale.status == status)
            .order_by(Sale.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_daily_sales(self, date) -> list[Sale]:
        """Get sales for a specific date."""
        stmt = (
            select(Sale)
            .where(func.date(Sale.created_at) == date)
            .order_by(Sale.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_total_sales_amount(self, start_date=None, end_date=None) -> float:
        """Get total sales amount for a date range."""
        stmt = select(func.sum(Sale.final_amount))

        if start_date:
            stmt = stmt.where(Sale.created_at >= start_date)
        if end_date:
            stmt = stmt.where(Sale.created_at <= end_date)

        result = await self.session.execute(stmt)
        return result.scalar() or 0.0


class SaleItemRepository(BaseRepository[SaleItem]):
    """Sale item repository."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize sale item repository."""
        super().__init__(SaleItem, session)

    async def get_by_sale(self, sale_id: UUID) -> list[SaleItem]:
        """Get sale items by sale ID."""
        stmt = select(SaleItem).where(SaleItem.sale_id == sale_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_product(self, product_id: UUID, skip: int = 0, limit: int = 20) -> list[SaleItem]:
        """Get sale items by product ID."""
        stmt = (
            select(SaleItem)
            .where(SaleItem.product_id == product_id)
            .order_by(SaleItem.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
