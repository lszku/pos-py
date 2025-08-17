"""Sale service."""

from datetime import datetime
from decimal import Decimal
from typing import Any, Optional, Union
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from ..repositories.sale import SaleItemRepository, SaleRepository
from ..schemas.sale import SaleCreate, SaleUpdate


class SaleService:
    """Sale service for business logic."""

    def __init__(self, session: AsyncSession) -> None:
        """Initialize sale service."""
        self.session = session
        self.sale_repo = SaleRepository(session)
        self.sale_item_repo = SaleItemRepository(session)

    async def create_sale(self, sale_data: SaleCreate, user_id: Union[str, UUID]) -> dict[str, Any]:
        """Create a new sale."""
        # Generate reference if not provided
        if not sale_data.reference:
            sale_data.reference = f"SALE-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        # Set final_amount if not provided
        if sale_data.final_amount is None:
            sale_data.final_amount = Decimal(sale_data.total_amount)

        # Convert user_id to UUID if it's a string
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        # Create sale
        sale_dict = sale_data.model_dump()
        sale_dict["total_amount"] = Decimal(sale_data.total_amount)
        sale_dict["final_amount"] = sale_data.final_amount
        sale_dict["created_by"] = user_id

        # Remove items from sale_dict as it's handled separately
        items = sale_dict.pop("items", [])

        sale = await self.sale_repo.create(**sale_dict)

        # Create sale items
        for item in items:
            item_dict = {
                "sale_id": sale.id,
                "product_id": UUID(item["product_id"]) if isinstance(item["product_id"], str) else item["product_id"],
                "quantity": item["quantity"],
                "unit_price": Decimal(item["unit_price"]),
                "total_amount": Decimal(item["unit_price"]) * item["quantity"]
            }
            await self.sale_item_repo.create(**item_dict)

        # Return sale with items
        result = {
            "id": str(sale.id),
            "reference": sale.reference,
            "customer_name": sale.customer_name,
            "customer_email": sale.customer_email,
            "total_amount": str(sale.total_amount),
            "discount_amount": str(sale.discount_amount),
            "tax_amount": str(sale.tax_amount),
            "final_amount": str(sale.final_amount),
            "status": sale.status,
            "payment_method": sale.payment_method,
            "notes": sale.notes,
            "created_by": str(sale.created_by),
            "created_at": sale.created_at,
            "completed_at": sale.completed_at,
            "items": items
        }
        return result

    async def get_sale(self, sale_id: UUID) -> Optional[dict[str, Any]]:
        """Get sale by ID."""
        sale = await self.sale_repo.get(sale_id)
        if sale:
            return {
                "id": str(sale.id),
                "reference": sale.reference,
                "total_amount": str(sale.total_amount),
                "payment_method": sale.payment_method,
                "created_at": sale.created_at
            }
        return None

    async def get_sales_by_user(self, user_id: Union[str, UUID], skip: int = 0, limit: int = 20) -> list[dict[str, Any]]:
        """Get sales by user ID."""
        # Convert user_id to UUID if it's a string
        if isinstance(user_id, str):
            user_id = UUID(user_id)

        sales = await self.sale_repo.get_by_user(user_id, skip, limit)
        result = []
        for sale in sales:
            result.append({
                "id": str(sale.id),
                "reference": sale.reference,
                "customer_name": sale.customer_name,
                "customer_email": sale.customer_email,
                "total_amount": str(sale.total_amount),
                "discount_amount": str(sale.discount_amount),
                "tax_amount": str(sale.tax_amount),
                "final_amount": str(sale.final_amount),
                "status": sale.status,
                "payment_method": sale.payment_method,
                "notes": sale.notes,
                "created_by": str(sale.created_by),
                "created_at": sale.created_at,
                "completed_at": sale.completed_at
            })
        return result

    async def update_sale(self, sale_id: UUID, sale_data: SaleUpdate) -> Optional[dict[str, Any]]:
        """Update sale."""
        update_data = sale_data.model_dump(exclude_unset=True)
        sale = await self.sale_repo.update(sale_id, **update_data)
        if sale:
            return {
                "id": str(sale.id),
                "reference": sale.reference,
                "total_amount": str(sale.total_amount),
                "payment_method": sale.payment_method,
                "created_at": sale.created_at
            }
        return None

    async def get_total_sales_amount(self, start_date=None, end_date=None) -> float:
        """Get total sales amount for a date range."""
        return await self.sale_repo.get_total_sales_amount(start_date, end_date)
