from pydantic import BaseModel
from datetime import datetime

class TableBase(BaseModel):
    """Base para mesa"""
    table_number: int
    capacity: int
    status: str = "available"  # 'available', 'occupied', 'reserved'

class TableCreate(TableBase):
    """Modelo para crear mesa"""
    pass

class Table(TableBase):
    """Modelo completo de mesa"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True