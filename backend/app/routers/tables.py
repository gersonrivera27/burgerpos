
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
import psycopg2

from ..database import get_db
from ..models import Table, TableCreate

router = APIRouter()

@router.get("", response_model=List[Table])
def get_tables(status: Optional[str] = None, conn = Depends(get_db)):
    """Obtener todas las mesas"""
    cursor = conn.cursor()
    if status:
        cursor.execute("SELECT * FROM tables WHERE status = %s ORDER BY table_number", (status,))
    else:
        cursor.execute("SELECT * FROM tables ORDER BY table_number")
    tables = cursor.fetchall()
    return tables

@router.post("", response_model=Table, status_code=status.HTTP_201_CREATED)
def create_table(table: TableCreate, conn = Depends(get_db)):
    """Crear una nueva mesa"""
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO tables (table_number, capacity, status) VALUES (%s, %s, %s) RETURNING *",
            (table.table_number, table.capacity, table.status)
        )
        new_table = cursor.fetchone()
        conn.commit()
        return new_table
    except psycopg2.IntegrityError:
        conn.rollback()
        raise HTTPException(status_code=400, detail="El número de mesa ya existe")

@router.patch("/{table_id}/status")
def update_table_status(table_id: int, status: str, conn = Depends(get_db)):
    """Actualizar el estado de una mesa"""
    valid_statuses = ['available', 'occupied', 'reserved']
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"Estado inválido. Debe ser: {', '.join(valid_statuses)}")
    
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE tables SET status = %s WHERE id = %s RETURNING *",
        (status, table_id)
    )
    updated_table = cursor.fetchone()
    
    if not updated_table:
        raise HTTPException(status_code=404, detail="Mesa no encontrada")
    
    conn.commit()
    return updated_table