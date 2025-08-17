"""Product repository with search and filtering methods."""

from typing import Optional

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.enums import ProductCategory

from ..models.product import Product
from .base import BaseRepository


class ProductRepository(BaseRepository[Product]):
    """Product repository with search and filtering methods."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize product repository."""
        super().__init__(Product, session)

    async def get_by_sku(self, sku: str) -> Optional[Product]:
        """Get product by SKU."""
        stmt = select(Product).where(Product.sku == sku)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def search_products(self, query: str, skip: int = 0, limit: int = 20) -> list[Product]:
        """Search products by name or SKU."""
        stmt = (
            select(Product)
            .where(
                or_(
                    Product.name.ilike(f"%{query}%"),
                    Product.sku.ilike(f"%{query}%")
                )
            )
            .where(Product.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_by_category(self, category: ProductCategory, skip: int = 0, limit: int = 20) -> list[Product]:
        """Get products by category."""
        stmt = (
            select(Product)
            .where(Product.category == category)
            .where(Product.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_active_products(self, skip: int = 0, limit: int = 20) -> list[Product]:
        """Get all active products."""
        stmt = (
            select(Product)
            .where(Product.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()
