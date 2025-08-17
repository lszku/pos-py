"""Product service."""

from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.enums import ProductCategory

from ..models.product import Product
from ..repositories.product import ProductRepository
from ..schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """Product service for business logic."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize product service."""
        self.session = session
        self.product_repo = ProductRepository(session)

    async def create_product(self, product_data: ProductCreate) -> Product:
        """Create a new product."""
        # Check if SKU already exists
        existing_product = await self.product_repo.get_by_sku(product_data.sku)
        if existing_product:
            raise ValueError(f"Product with SKU {product_data.sku} already exists")

        product = await self.product_repo.create(**product_data.model_dump())
        return product

    async def get_product(self, product_id: UUID) -> Optional[Product]:
        """Get product by ID."""
        return await self.product_repo.get(product_id)

    async def get_products(self, skip: int = 0, limit: int = 20) -> list[Product]:
        """Get all active products."""
        return await self.product_repo.get_active_products(skip, limit)

    async def search_products(self, query: str, skip: int = 0, limit: int = 20) -> list[Product]:
        """Search products by name or SKU."""
        return await self.product_repo.search_products(query, skip, limit)

    async def get_products_by_category(self, category: ProductCategory,
                                     skip: int = 0, limit: int = 20) -> list[Product]:
        """Get products by category."""
        return await self.product_repo.get_by_category(category, skip, limit)

    async def update_product(self, product_id: UUID, product_data: ProductUpdate) -> Optional[Product]:
        """Update product."""
        update_data = product_data.model_dump(exclude_unset=True)
        return await self.product_repo.update(product_id, **update_data)

    async def delete_product(self, product_id: UUID) -> bool:
        """Delete product (soft delete by setting is_active to False)."""
        return await self.product_repo.update(product_id, is_active=False) is not None
