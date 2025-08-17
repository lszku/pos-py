"""Product API endpoints."""

from typing import Any, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from shared.models.enums import ProductCategory

from ..core.database import get_db
from ..core.security import get_current_user
from ..schemas.product import ProductCreate, ProductResponse, ProductUpdate
from ..services.product import ProductService

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new product."""
    product_service = ProductService(db)

    try:
        product = await product_service.create_product(product_data)
        return product
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/", response_model=list[ProductResponse])
async def get_products(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of records to return"),
    category: Optional[ProductCategory] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search by name or SKU"),
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get products with pagination and filtering."""
    product_service = ProductService(db)

    if search:
        products = await product_service.search_products(search, skip, limit)
    elif category:
        products = await product_service.get_products_by_category(category, skip, limit)
    else:
        products = await product_service.get_products(skip, limit)

    return products


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific product by ID."""
    product_service = ProductService(db)
    product = await product_service.get_product(product_id)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: UUID,
    product_data: ProductUpdate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Update a product."""
    product_service = ProductService(db)
    product = await product_service.update_product(product_id, product_data)

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


@router.delete("/{product_id}")
async def delete_product(
    product_id: UUID,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """Delete a product (soft delete)."""
    product_service = ProductService(db)
    success = await product_service.delete_product(product_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return {"message": "Product deleted successfully"}


@router.get("/categories/list")
async def get_categories() -> Any:
    """Get all available product categories."""
    return [{"value": category.value, "label": category.value.replace("_", " ").title()}
            for category in ProductCategory]
