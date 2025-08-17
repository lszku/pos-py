"""Stock API endpoints."""

from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.database import get_db
from ..core.security import get_current_user
from ..schemas.stock import (
    StockCreate,
    StockEntryCreate,
    StockEntryResponse,
    StockResponse,
    StockUpdate,
)
from ..services.stock import StockService

router = APIRouter(prefix="/stock", tags=["stock"])


@router.post("/", response_model=StockResponse)
async def create_stock(
    stock_data: StockCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new stock item."""
    stock_service = StockService(db)
    stock = await stock_service.create_stock(stock_data)
    return stock


@router.get("/", response_model=list[StockResponse])
async def get_stock_items(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    product_id: Optional[UUID] = Query(None, description="Filter by product ID"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get stock items with pagination."""
    stock_service = StockService(db)

    if product_id:
        stock_items = await stock_service.get_stock_by_product(product_id)
    else:
        stock_items = await stock_service.get_stock_list(skip, limit)

    return stock_items


@router.get("/{stock_id}", response_model=StockResponse)
async def get_stock_item(
    stock_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific stock item by ID."""
    stock_service = StockService(db)
    stock = await stock_service.get_stock(stock_id)

    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock item not found"
        )

    return stock


@router.put("/{stock_id}", response_model=StockResponse)
async def update_stock_item(
    stock_id: UUID,
    stock_data: StockUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update a stock item."""
    stock_service = StockService(db)
    stock = await stock_service.update_stock_quantity(stock_id, stock_data.quantity or 0)

    if not stock:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock item not found"
        )

    return stock


@router.get("/product/{product_id}/available")
async def get_available_stock(
    product_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get available stock quantity for a product."""
    stock_service = StockService(db)
    quantity = await stock_service.get_available_stock(product_id)
    return {"product_id": str(product_id), "available_quantity": quantity}


@router.get("/low-stock")
async def get_low_stock_products(
    threshold: int = Query(10, ge=1, description="Low stock threshold"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get products with low stock."""
    stock_service = StockService(db)
    low_stock_items = await stock_service.get_low_stock_products(threshold)
    return low_stock_items


# Stock Entry endpoints
@router.post("/entries", response_model=StockEntryResponse)
async def create_stock_entry(
    entry_data: StockEntryCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new stock entry."""
    stock_service = StockService(db)
    entry = await stock_service.create_stock_entry(entry_data, current_user["user_id"])
    return entry


@router.get("/entries/incomplete", response_model=list[StockEntryResponse])
async def get_incomplete_entries(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get incomplete stock entries for the current user."""
    stock_service = StockService(db)
    entries = await stock_service.get_incomplete_entries(current_user["user_id"])
    return entries


@router.post("/entries/{entry_id}/complete")
async def complete_stock_entry(
    entry_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Complete a stock entry."""
    stock_service = StockService(db)
    entry = await stock_service.complete_stock_entry(entry_id)

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Stock entry not found"
        )

    return {"message": "Stock entry completed successfully"}
