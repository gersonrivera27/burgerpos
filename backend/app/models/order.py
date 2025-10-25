"""
Modelos Pydantic para Órdenes
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class OrderItemModifier(BaseModel):
    """Modificador de un item"""
    modifier_id: int
    quantity: int = 1

class OrderItemCreate(BaseModel):
    """Modelo para crear item de orden"""
    product_id: int
    quantity: int = Field(..., gt=0)
    special_instructions: Optional[str] = None
    modifiers: Optional[List[OrderItemModifier]] = []

class OrderItemResponse(BaseModel):
    """Respuesta de item de orden"""
    id: int
    product_id: int
    product_name: str
    quantity: int
    unit_price: float
    subtotal: float
    special_instructions: Optional[str]
    modifiers: Optional[List[dict]] = []

class OrderCreate(BaseModel):
    """Modelo para crear orden"""
    customer_name: Optional[str] = None
    order_type: str  # 'dine-in', 'takeout', 'delivery'
    table_id: Optional[int] = None
    items: List[OrderItemCreate]
    payment_method: Optional[str] = None
    notes: Optional[str] = None

class OrderUpdate(BaseModel):
    """Modelo para actualizar orden"""
    status: Optional[str] = None
    payment_method: Optional[str] = None

class OrderResponse(BaseModel):
    """Respuesta completa de orden"""
    id: int
    order_number: str
    customer_name: Optional[str]
    order_type: str
    status: str
    subtotal: float
    tax: float
    discount: float
    total: float
    payment_method: Optional[str]
    notes: Optional[str]
    created_at: datetime
    completed_at: Optional[datetime]

    class Config:
        from_attributes = True

class UpdateOrderPaymentRequest(BaseModel):
    """Modelo para actualizar método de pago"""
    payment_method: str

class OrderItemDto(BaseModel):
    """DTO para items al crear orden (recall)"""
    product_id: int
    quantity: int
    special_instructions: Optional[str] = None

class CreateOrderRequest(BaseModel):
    """Modelo para crear orden desde historial (recall)"""
    customer_name: str = ""
    order_type: str = "dine-in"
    notes: Optional[str] = None
    items: List[OrderItemDto]