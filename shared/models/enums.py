"""Enums for the POS application."""

from enum import Enum


class ProductCategory(str, Enum):
    """Product categories for animal accessories and food."""

    DOG_FOOD = "dog_food"
    CAT_FOOD = "cat_food"
    BIRD_FOOD = "bird_food"
    FISH_FOOD = "fish_food"
    REPTILE_FOOD = "reptile_food"
    DOG_ACCESSORIES = "dog_accessories"
    CAT_ACCESSORIES = "cat_accessories"
    BIRD_ACCESSORIES = "bird_accessories"
    FISH_ACCESSORIES = "fish_accessories"
    REPTILE_ACCESSORIES = "reptile_accessories"
    TOYS = "toys"
    HEALTH_CARE = "health_care"
    GROOMING = "grooming"
    BEDDING = "bedding"
    OTHER = "other"


class StockStatus(str, Enum):
    """Stock status enumeration."""

    AVAILABLE = "available"
    LOW_STOCK = "low_stock"
    OUT_OF_STOCK = "out_of_stock"
    DISCONTINUED = "discontinued"


class SaleStatus(str, Enum):
    """Sale status enumeration."""

    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class UserRole(str, Enum):
    """User role enumeration."""

    ADMIN = "admin"
    MANAGER = "manager"
    CASHIER = "cashier"
    VIEWER = "viewer" 