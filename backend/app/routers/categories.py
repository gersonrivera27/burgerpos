"""
Router para gestión de categorías
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List

from ..database import get_db
from ..models import Category, CategoryCreate

router = APIRouter()

@router.get("", response_model=List[Category])
def get_categories(conn = Depends(get_db)):
    """Obtener todas las categorías"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories ORDER BY name")
    categories = cursor.fetchall()
    return categories

@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, conn = Depends(get_db)):
    """Obtener una categoría por ID"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM categories WHERE id = %s", (category_id,))
    category = cursor.fetchone()
    if not category:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return category

@router.post("", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, conn = Depends(get_db)):
    """Crear una nueva categoría"""
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO categories (name, description) VALUES (%s, %s) RETURNING *",
        (category.name, category.description)
    )
    new_category = cursor.fetchone()
    conn.commit()
    return new_category