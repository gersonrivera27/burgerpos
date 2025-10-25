"""
Router para gestión de modificadores
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
import psycopg2

from ..database import get_db
from ..models import Modifier, ModifierCreate

router = APIRouter()

@router.get("", response_model=List[Modifier])
def get_modifiers(conn = Depends(get_db)):
    """Obtener todos los modificadores"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM modifiers ORDER BY modifier_type, name")
    modifiers = cursor.fetchall()
    return modifiers

@router.post("", response_model=Modifier, status_code=status.HTTP_201_CREATED)
def create_modifier(modifier: ModifierCreate, conn = Depends(get_db)):
    """Crear un nuevo modificador"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO modifiers (name, price, modifier_type) VALUES (%s, %s, %s) RETURNING *",
        (modifier.name, modifier.price, modifier.modifier_type)
    )
    new_modifier = cursor.fetchone()
    conn.commit()
    return new_modifier
