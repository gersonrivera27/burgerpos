from pydantic import BaseModel
from datetime import datetime

class ModifierBase(BaseModel):
    """Base para modificador"""
    name: str
    price: float = 0.00
    modifier_type: str  # 'extra', 'remove', 'substitute'

class ModifierCreate(ModifierBase):
    """Modelo para crear modificador"""
    pass

class Modifier(ModifierBase):
    """Modelo completo de modificador"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True