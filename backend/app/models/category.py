
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CategoryBase(BaseModel):
    """Base para categoría"""
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    """Modelo para crear categoría"""
    pass

class Category(CategoryBase):
    """Modelo completo de categoría"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True