"""
Modelos Pydantic para Productos
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class ProductBase(BaseModel):
    """Base para producto"""
    category_id: int
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    image_url: Optional[str] = None
    is_available: bool = True

class ProductCreate(ProductBase):
    """Modelo para crear producto"""
    pass

class ProductUpdate(BaseModel):
    """Modelo para actualizar producto"""
    category_id: Optional[int] = None
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None

class Product(ProductBase):
    """Modelo completo de producto"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True