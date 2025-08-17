"""Stock management service."""

from typing import Any, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories.product import ProductRepository
from ..repositories.stock import StockRepository
from ..schemas.stock import StockCreate, StockUpdate


class StockService:
    """Stock management service for inventory control."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize stock service."""
        self.session = session
        self.stock_repo = StockRepository(session)
        self.product_repo = ProductRepository(session)

    async def create_stock_entry(self, stock_data: StockCreate, user_id: UUID) -> dict[str, Any]:
        """Create a new stock entry."""
        # Verify product exists
        product = await self.product_repo.get(stock_data.product_id)
        if not product:
            raise ValueError("Product not found")

        # Create stock entry
        stock = await self.stock_repo.create(**stock_data.model_dump())

        return {
            "id": str(stock.id),
            "product_id": str(stock.product_id),
            "product_name": product.name,
            "quantity": stock.quantity,
            "location": stock.location,
            "created_at": stock.created_at.isoformat()
        }

    async def create_stock(self, stock_data: StockCreate) -> dict[str, Any]:
        """Create a new stock item."""
        # Verify product exists
        product = await self.product_repo.get(stock_data.product_id)
        if not product:
            raise ValueError("Product not found")

        # Create stock entry
        stock = await self.stock_repo.create(**stock_data.model_dump())

        return {
            "id": str(stock.id),
            "product_id": str(stock.product_id),
            "product_name": product.name,
            "quantity": stock.quantity,
            "location": stock.location,
            "status": stock.status,
            "created_at": stock.created_at.isoformat()
        }

    async def get_stock_by_id(self, stock_id: UUID) -> Optional[dict[str, Any]]:
        """Get stock entry by ID."""
        stock = await self.stock_repo.get(stock_id)
        if not stock:
            return None

        product = await self.product_repo.get(stock.product_id)

        return {
            "id": str(stock.id),
            "product_id": str(stock.product_id),
            "product_name": product.name if product else "Unknown",
            "quantity": stock.quantity,
            "location": stock.location,
            "status": stock.status,
            "created_at": stock.created_at.isoformat(),
            "updated_at": stock.updated_at.isoformat() if stock.updated_at else None
        }

    async def get_stock(self, stock_id: UUID) -> Optional[dict[str, Any]]:
        """Get stock entry by ID (alias for get_stock_by_id)."""
        return await self.get_stock_by_id(stock_id)

    async def get_stock_by_product(self, product_id: UUID) -> list[dict[str, Any]]:
        """Get stock entries by product ID."""
        stock_entries = await self.stock_repo.get_by_product(product_id)

        result = []
        for stock in stock_entries:
            product = await self.product_repo.get(stock.product_id)
            result.append({
                "id": str(stock.id),
                "product_id": str(stock.product_id),
                "product_name": product.name if product else "Unknown",
                "quantity": stock.quantity,
                "location": stock.location,
                "status": stock.status,
                "created_at": stock.created_at.isoformat()
            })

        return result

    async def update_stock_quantity(self, stock_id: UUID, quantity: int) -> Optional[dict[str, Any]]:
        """Update stock quantity."""
        stock = await self.stock_repo.get(stock_id)
        if not stock:
            return None

        # Update stock quantity
        updated_stock = await self.stock_repo.update_stock_quantity(stock_id, quantity)
        if not updated_stock:
            return None

        product = await self.product_repo.get(updated_stock.product_id)

        return {
            "id": str(updated_stock.id),
            "product_id": str(updated_stock.product_id),
            "product_name": product.name if product else "Unknown",
            "quantity": updated_stock.quantity,
            "location": updated_stock.location,
            "created_at": updated_stock.created_at.isoformat(),
            "updated_at": updated_stock.updated_at.isoformat() if updated_stock.updated_at else None
        }

    async def get_stock_list(self, skip: int = 0, limit: int = 100) -> list[dict[str, Any]]:
        """Get paginated list of stock entries."""
        stock_entries = await self.stock_repo.get_all(skip=skip, limit=limit)

        result = []
        for stock in stock_entries:
            product = await self.product_repo.get(stock.product_id)
            result.append({
                "id": str(stock.id),
                "product_id": str(stock.product_id),
                "product_name": product.name if product else "Unknown",
                "quantity": stock.quantity,
                "location": stock.location,
                "status": stock.status,
                "created_at": stock.created_at.isoformat()
            })

        return result

    async def update_stock_entry(self, stock_id: UUID, stock_data: StockUpdate) -> Optional[dict[str, Any]]:
        """Update a stock entry."""
        stock = await self.stock_repo.get(stock_id)
        if not stock:
            return None

        # Update stock entry
        updated_stock = await self.stock_repo.update(stock_id, **stock_data.model_dump(exclude_unset=True))

        product = await self.product_repo.get(updated_stock.product_id)

        return {
            "id": str(updated_stock.id),
            "product_id": str(updated_stock.product_id),
            "product_name": product.name if product else "Unknown",
            "quantity": updated_stock.quantity,
            "location": updated_stock.location,
            "created_at": updated_stock.created_at.isoformat(),
            "updated_at": updated_stock.updated_at.isoformat() if updated_stock.updated_at else None
        }

    async def get_available_stock(self, product_id: UUID) -> int:
        """Get total available stock for a product."""
        stock_entries = await self.stock_repo.get_by_product(product_id)
        return sum(stock.quantity for stock in stock_entries)

    async def get_low_stock_products(self, threshold: int = 10) -> list[dict[str, Any]]:
        """Get products with low stock levels."""
        products = await self.product_repo.get_active_products()
        low_stock_products = []

        for product in products:
            available_stock = await self.get_available_stock(product.id)
            if available_stock <= threshold:
                low_stock_products.append({
                    "product_id": str(product.id),
                    "product_name": product.name,
                    "sku": product.sku,
                    "available_stock": available_stock,
                    "threshold": threshold
                })

        return low_stock_products

    async def get_stock_by_location(self, location: str) -> list[dict[str, Any]]:
        """Get stock entries by location."""
        stock_entries = await self.stock_repo.get_by_product(location)  # This needs to be fixed

        result = []
        for stock in stock_entries:
            product = await self.product_repo.get(stock.product_id)
            result.append({
                "id": str(stock.id),
                "product_id": str(stock.product_id),
                "product_name": product.name if product else "Unknown",
                "quantity": stock.quantity,
                "location": stock.location,
                "notes": stock.notes,
                "created_at": stock.created_at.isoformat()
            })

        return result

    async def get_stock_summary(self) -> dict[str, Any]:
        """Get stock summary statistics."""
        all_stock = await self.stock_repo.get_all_stock()

        total_items = len(all_stock)
        total_quantity = sum(stock.quantity for stock in all_stock)

        # Group by location
        location_summary = {}
        for stock in all_stock:
            if stock.location not in location_summary:
                location_summary[stock.location] = 0
            location_summary[stock.location] += stock.quantity

        # Get low stock products
        low_stock_products = await self.get_low_stock_products()

        return {
            "total_items": total_items,
            "total_quantity": total_quantity,
            "location_summary": location_summary,
            "low_stock_products": low_stock_products,
            "low_stock_count": len(low_stock_products)
        }

    async def search_stock(self, query: str) -> list[dict[str, Any]]:
        """Search stock entries by product name or location."""
        # Get all products that match the search query
        products = await self.product_repo.search_products(query)
        product_ids = [product.id for product in products]

        # Get stock entries for matching products
        stock_entries = []
        for product_id in product_ids:
            product_stock = await self.stock_repo.get_stock_by_product(product_id)
            stock_entries.extend(product_stock)

        # Also search by location
        location_stock = await self.stock_repo.get_stock_by_location(query)
        stock_entries.extend(location_stock)

        # Remove duplicates and format results
        seen_ids = set()
        result = []

        for stock in stock_entries:
            if stock.id not in seen_ids:
                seen_ids.add(stock.id)
                product = await self.product_repo.get(stock.product_id)
                result.append({
                    "id": str(stock.id),
                    "product_id": str(stock.product_id),
                    "product_name": product.name if product else "Unknown",
                    "quantity": stock.quantity,
                    "location": stock.location,
                    "notes": stock.notes,
                    "created_at": stock.created_at.isoformat()
                })

        return result
