"""
Router para gestión de productos
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional

from ..database import get_db
from ..models import Product, ProductCreate, ProductUpdate

router = APIRouter()

@router.get("", response_model=List[Product])
def get_products(
    category_id: Optional[int] = None,
    available_only: bool = True,
    conn = Depends(get_db)
):
    """Obtener todos los productos, con filtros opcionales"""
    cursor = conn.cursor()
    
    if category_id:
        query = "SELECT * FROM products WHERE category_id = %s"
        params = [category_id]
    else:
        query = "SELECT * FROM products WHERE 1=1"
        params = []
    
    if available_only:
        query += " AND is_available = true"
    
    query += " ORDER BY category_id, name"
    
    cursor.execute(query, params)
    products = cursor.fetchall()
    return products

@router.get("/{product_id}", response_model=Product)
def get_product(product_id: int, conn = Depends(get_db)):
    """Obtener un producto por ID"""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
    product = cursor.fetchone()
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return product

@router.post("", response_model=Product, status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate, conn = Depends(get_db)):
    """Crear un nuevo producto"""
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO products (category_id, name, description, price, image_url, is_available) 
           VALUES (%s, %s, %s, %s, %s, %s) RETURNING *""",
        (product.category_id, product.name, product.description, 
         product.price, product.image_url, product.is_available)
    )
    new_product = cursor.fetchone()
    conn.commit()
    return new_product

@router.put("/{product_id}", response_model=Product)
def update_product(product_id: int, product: ProductUpdate, conn = Depends(get_db)):
    """Actualizar un producto"""
    cursor = conn.cursor()
    
    # Construir query dinámicamente solo con campos que se enviaron
    updates = []
    values = []
    
    if product.category_id is not None:
        updates.append("category_id = %s")
        values.append(product.category_id)
    if product.name is not None:
        updates.append("name = %s")
        values.append(product.name)
    if product.description is not None:
        updates.append("description = %s")
        values.append(product.description)
    if product.price is not None:
        updates.append("price = %s")
        values.append(product.price)
    if product.image_url is not None:
        updates.append("image_url = %s")
        values.append(product.image_url)
    if product.is_available is not None:
        updates.append("is_available = %s")
        values.append(product.is_available)
    
    if not updates:
        raise HTTPException(status_code=400, detail="No hay campos para actualizar")
    
    updates.append("updated_at = CURRENT_TIMESTAMP")
    values.append(product_id)
    
    query = f"UPDATE products SET {', '.join(updates)} WHERE id = %s RETURNING *"
    cursor.execute(query, values)
    updated_product = cursor.fetchone()
    
    if not updated_product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    conn.commit()
    return updated_product

@router.delete("/{product_id}")
def delete_product(product_id: int, conn = Depends(get_db)):
    """Eliminar un producto (soft delete - marca como no disponible)"""
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE products SET is_available = false WHERE id = %s RETURNING id",
        (product_id,)
    )
    deleted = cursor.fetchone()
    
    if not deleted:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    conn.commit()
    return {"message": "Producto eliminado correctamente", "id": product_id}