"""
Database Schemas

Define your MongoDB collection schemas here using Pydantic models.
These schemas are used for data validation in your application.

Each Pydantic model represents a collection in your database.
Model name is converted to lowercase for the collection name:
- User -> "user" collection
- Product -> "product" collection
- BlogPost -> "blogs" collection
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

# Core ecommerce schemas for a Nike-like store

class Category(BaseModel):
    """
    Categories collection schema
    Collection name: "category"
    """
    name: str = Field(..., description="Category name, e.g., 'Shoes'")
    slug: str = Field(..., description="URL friendly identifier")
    image: Optional[HttpUrl] = Field(None, description="Hero image for the category")

class Product(BaseModel):
    """
    Products collection schema
    Collection name: "product"
    """
    title: str = Field(..., description="Product title")
    description: Optional[str] = Field(None, description="Product description")
    price: float = Field(..., ge=0, description="Price in dollars")
    category: str = Field(..., description="Product category name")
    brand: str = Field("Nike", description="Brand name")
    images: List[HttpUrl] = Field(default_factory=list, description="Image gallery URLs")
    colors: List[str] = Field(default_factory=list, description="Available colorways")
    sizes: List[str] = Field(default_factory=list, description="Available sizes")
    rating: float = Field(4.5, ge=0, le=5, description="Average rating")
    featured: bool = Field(False, description="Feature on home page")
    in_stock: bool = Field(True, description="Whether product is in stock")

class User(BaseModel):
    """
    Users collection schema
    Collection name: "user" (lowercase of class name)
    """
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    address: str = Field(..., description="Address")
    age: Optional[int] = Field(None, ge=0, le=120, description="Age in years")
    is_active: bool = Field(True, description="Whether user is active")
