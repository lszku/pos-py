"""Sales API endpoints."""

from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..core.security import get_current_user
from ..schemas.sale import SaleCreate, SaleResponse, SaleUpdate
from ..services.sale import SaleService

router = APIRouter(prefix="/sales", tags=["sales"])


@router.post("/", response_model=SaleResponse)
async def create_sale(
    sale_data: SaleCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new sale."""
    sale_service = SaleService(db)
    sale = await sale_service.create_sale(sale_data, current_user["user_id"])
    return sale


@router.get("/", response_model=list[SaleResponse])
async def get_sales(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get sales with pagination."""
    sale_service = SaleService(db)
    sales = await sale_service.get_sales_by_user(current_user["user_id"], skip, limit)
    return sales


@router.get("/{sale_id}", response_model=SaleResponse)
async def get_sale(
    sale_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific sale by ID."""
    sale_service = SaleService(db)
    sale = await sale_service.get_sale(sale_id)

    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )

    return sale


@router.put("/{sale_id}", response_model=SaleResponse)
async def update_sale(
    sale_id: UUID,
    sale_data: SaleUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update a sale."""
    sale_service = SaleService(db)
    sale = await sale_service.update_sale(sale_id, sale_data)

    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sale not found"
        )

    return sale


@router.get("/stats/total")
async def get_total_sales(
    start_date: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get total sales amount for a date range."""
    sale_service = SaleService(db)
    total = await sale_service.get_total_sales_amount(start_date, end_date)
    return {"total_amount": total}
