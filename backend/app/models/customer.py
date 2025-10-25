"""
Modelos Pydantic para Clientes
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class CustomerBase(BaseModel):
    """Base para cliente"""
    phone: str
    name: str
    email: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: str = "Drogheda"
    county: str = "Louth"
    eircode: Optional[str] = None
    country: str = "Ireland"
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None

class CustomerCreate(CustomerBase):
    """Modelo para crear cliente"""
    pass

class CustomerUpdate(BaseModel):
    """Modelo para actualizar cliente"""
    phone: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    address_line1: Optional[str] = None
    address_line2: Optional[str] = None
    city: Optional[str] = None
    county: Optional[str] = None
    eircode: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    notes: Optional[str] = None
    is_active: Optional[bool] = None

class Customer(CustomerBase):
    """Modelo completo de cliente"""
    id: int
    is_active: bool = True
    total_orders: int = 0
    total_spent: float = 0.00
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
