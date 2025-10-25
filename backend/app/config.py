"""
Configuración de la aplicación
"""
import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Configuración de la aplicación"""
    
    # Base de datos
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:postgres@db:5432/burger_pos"
    )
    
    # API
    API_TITLE: str = "Burger POS API"
    API_VERSION: str = "1.0.0"
    API_DESCRIPTION: str = "API completa para sistema POS de restaurante de hamburguesas"
    
    # CORS
    ALLOWED_ORIGINS: list = ["*"]
    
    # Configuración de negocio
    TAX_RATE: float = 0.10  # 10% de impuestos
    
    class Config:
        case_sensitive = True

settings = Settings()