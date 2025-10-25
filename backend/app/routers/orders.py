"""
Router para gestión de órdenes
"""
from fastapi import APIRouter, HTTPException, Depends, status
from typing import List, Optional
from datetime import datetime, date

from ..database import get_db
from ..models import (
    OrderCreate, OrderResponse, OrderUpdate, 
    UpdateOrderPaymentRequest, CreateOrderRequest
)
from ..config import settings

router = APIRouter()

@router.post("", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, conn = Depends(get_db)):
    """Crear una nueva orden"""
    cursor = conn.cursor()
    
    if not order.items:
        raise HTTPException(status_code=400, detail="La orden debe tener al menos un item")
    
    # Generar número de orden único
    cursor.execute("SELECT COUNT(*) as count FROM orders WHERE DATE(created_at) = CURRENT_DATE")
    count = cursor.fetchone()['count']
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{count + 1:04d}"
    
    # Calcular totales
    subtotal = 0
    for item in order.items:
        cursor.execute("SELECT price FROM products WHERE id = %s AND is_available = true", (item.product_id,))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail=f"Producto {item.product_id} no encontrado o no disponible")
        
        item_price = float(product['price']) * item.quantity
        
        # Agregar precio de modificadores
        if item.modifiers:
            for mod in item.modifiers:
                cursor.execute("SELECT price FROM modifiers WHERE id = %s", (mod.modifier_id,))
                modifier = cursor.fetchone()
                if modifier:
                    item_price += float(modifier['price']) * mod.quantity * item.quantity
        
        subtotal += item_price
    
    tax = subtotal * settings.TAX_RATE
    total = subtotal + tax
    
    # Crear orden
    cursor.execute(
        """INSERT INTO orders (order_number, customer_name, order_type, table_id, 
           subtotal, tax, total, payment_method, notes, status) 
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING *""",
        (order_number, order.customer_name, order.order_type, order.table_id,
         subtotal, tax, total, order.payment_method, order.notes, 'pending')
    )
    new_order = cursor.fetchone()
    order_id = new_order['id']
    
    # Si la orden es para una mesa, marcar mesa como ocupada
    if order.table_id:
        cursor.execute("UPDATE tables SET status = 'occupied' WHERE id = %s", (order.table_id,))
    
    # Insertar items de la orden
    for item in order.items:
        cursor.execute("SELECT price FROM products WHERE id = %s", (item.product_id,))
        product = cursor.fetchone()
        unit_price = float(product['price'])
        item_subtotal = unit_price * item.quantity
        
        cursor.execute(
            """INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal, special_instructions)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING id""",
            (order_id, item.product_id, item.quantity, unit_price, item_subtotal, item.special_instructions)
        )
        order_item_id = cursor.fetchone()['id']
        
        # Insertar modificadores del item
        if item.modifiers:
            for mod in item.modifiers:
                cursor.execute("SELECT price FROM modifiers WHERE id = %s", (mod.modifier_id,))
                modifier = cursor.fetchone()
                if modifier:
                    cursor.execute(
                        """INSERT INTO order_item_modifiers (order_item_id, modifier_id, quantity, price)
                           VALUES (%s, %s, %s, %s)""",
                        (order_item_id, mod.modifier_id, mod.quantity, float(modifier['price']))
                    )
    
    conn.commit()
    return new_order

@router.get("", response_model=List[OrderResponse])
def get_orders(
    status: Optional[str] = None,
    order_type: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    limit: int = 100,
    conn = Depends(get_db)
):
    """Obtener órdenes con filtros opcionales"""
    cursor = conn.cursor()
    
    query = "SELECT * FROM orders WHERE 1=1"
    params = []
    
    if status:
        query += " AND status = %s"
        params.append(status)
    
    if order_type:
        query += " AND order_type = %s"
        params.append(order_type)
    
    if date_from:
        query += " AND DATE(created_at) >= %s"
        params.append(date_from)
    
    if date_to:
        query += " AND DATE(created_at) <= %s"
        params.append(date_to)
    
    query += " ORDER BY created_at DESC LIMIT %s"
    params.append(limit)
    
    cursor.execute(query, params)
    orders = cursor.fetchall()
    return orders

@router.get("/{order_id}/details")
def get_order_detail(order_id: int, conn = Depends(get_db)):
    """Obtener detalle completo de una orden"""
    cursor = conn.cursor()
    
    # Obtener orden
    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    # Obtener items con sus productos
    cursor.execute(
        """SELECT oi.*, p.name as product_name, p.category_id as product_category
           FROM order_items oi 
           JOIN products p ON oi.product_id = p.id 
           WHERE oi.order_id = %s""",
        (order_id,)
    )
    items = cursor.fetchall()
    
    # Obtener modificadores de cada item
    for item in items:
        cursor.execute(
            """SELECT oim.*, m.name as modifier_name
               FROM order_item_modifiers oim
               JOIN modifiers m ON oim.modifier_id = m.id
               WHERE oim.order_item_id = %s""",
            (item['id'],)
        )
        item['modifiers'] = cursor.fetchall()
    
    return {
        "order": dict(order),
        "items": [dict(item) for item in items]
    }

@router.patch("/{order_id}/status")
def update_order_status(order_id: int, new_status: str, conn = Depends(get_db)):
    """Actualizar el estado de una orden"""
    valid_statuses = ['pending', 'preparing', 'ready', 'completed', 'cancelled']
    
    if new_status not in valid_statuses:
        raise HTTPException(
            status_code=400, 
            detail=f"Estado inválido. Debe ser: {', '.join(valid_statuses)}"
        )
    
    cursor = conn.cursor()
    
    # Obtener la orden actual
    cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
    order = cursor.fetchone()
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    # Actualizar orden
    update_query = "UPDATE orders SET status = %s"
    params = [new_status]
    
    # Si se completa la orden, agregar timestamp
    if new_status == 'completed':
        update_query += ", completed_at = CURRENT_TIMESTAMP"
        
        # Si había mesa, liberarla
        if order['table_id']:
            cursor.execute("UPDATE tables SET status = 'available' WHERE id = %s", (order['table_id'],))
    
    update_query += " WHERE id = %s RETURNING *"
    params.append(order_id)
    
    cursor.execute(update_query, params)
    updated_order = cursor.fetchone()
    conn.commit()
    
    return updated_order

@router.put("/{order_id}/payment")
def update_order_payment(
    order_id: int,
    payment_data: UpdateOrderPaymentRequest,
    conn = Depends(get_db)
):
    """Actualizar método de pago de una orden"""
    cursor = conn.cursor()
    
    order = cursor.fetchone("SELECT * FROM orders WHERE id = %s", (order_id,))
    if not order:
        raise HTTPException(status_code=404, detail="Orden no encontrada")
    
    # Actualizar payment method
    cursor.execute(
        "UPDATE orders SET payment_method = %s, updated_at = CURRENT_TIMESTAMP WHERE id = %s RETURNING *",
        (payment_data.payment_method, order_id)
    )
    updated_order = cursor.fetchone()
    conn.commit()
    
    return updated_order

@router.post("/recall", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def recall_order(order_data: CreateOrderRequest, conn = Depends(get_db)):
    """Crear nueva orden basada en una existente (recall)"""
    cursor = conn.cursor()
    
    if not order_data.items:
        raise HTTPException(status_code=400, detail="La orden debe tener al menos un item")
    
    # Generar número de orden
    cursor.execute("SELECT COUNT(*) as count FROM orders WHERE DATE(created_at) = CURRENT_DATE")
    count = cursor.fetchone()['count']
    order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{count + 1:04d}"
    
    # Calcular totales
    subtotal = 0
    items_to_create = []
    
    for item_data in order_data.items:
        # Get product
        cursor.execute("SELECT price FROM products WHERE id = %s AND is_available = true", (item_data.product_id,))
        product = cursor.fetchone()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item_data.product_id} not found or unavailable")
        
        item_subtotal = float(product['price']) * item_data.quantity
        subtotal += item_subtotal
        
        items_to_create.append({
            "product_id": item_data.product_id,
            "quantity": item_data.quantity,
            "unit_price": float(product['price']),
            "subtotal": item_subtotal,
            "special_instructions": item_data.special_instructions
        })
    
    # Calculate tax and total
    tax = subtotal * settings.TAX_RATE
    total = subtotal + tax
    
    # Create order
    cursor.execute(
        """INSERT INTO orders (order_number, customer_name, order_type, status, 
           subtotal, tax, discount, total, payment_method, notes, created_at, updated_at)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP) RETURNING *""",
        (order_number, order_data.customer_name, order_data.order_type, 'pending',
         subtotal, tax, 0, total, None, order_data.notes)
    )
    new_order = cursor.fetchone()
    order_id = new_order['id']
    
    # Create order items
    for item_data in items_to_create:
        cursor.execute(
            """INSERT INTO order_items (order_id, product_id, quantity, unit_price, subtotal, special_instructions)
               VALUES (%s, %s, %s, %s, %s, %s)""",
            (order_id, item_data['product_id'], item_data['quantity'], 
             item_data['unit_price'], item_data['subtotal'], item_data['special_instructions'])
        )
    
    conn.commit()
    return new_order