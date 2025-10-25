"""
Gestión de conexión a base de datos
"""
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings

def get_db():
    """
    Obtener conexión a la base de datos
    
    Yields:
        Connection: Conexión a PostgreSQL con RealDictCursor
    """
    conn = psycopg2.connect(
        settings.DATABASE_URL,
        cursor_factory=RealDictCursor
    )
    try:
        yield conn
    finally:
        conn.close()