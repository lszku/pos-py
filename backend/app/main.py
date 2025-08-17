"""Main FastAPI application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.auth import router as auth_router
from .api.products import router as products_router
from .api.sales import router as sales_router
from .api.stock import router as stock_router
from .core.config import settings

app = FastAPI(
    title=settings.app_name,
    description="Point of Sale API for animal accessories and food shop",
    version="0.1.0",
    debug=settings.debug,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(products_router)
app.include_router(stock_router)
app.include_router(sales_router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to POS API", "version": "0.1.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}
