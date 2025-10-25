
-- Tabla de Clientes
CREATE TABLE IF NOT EXISTS customers (
    id SERIAL PRIMARY KEY,
    phone VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    email VARCHAR(200),
    
    -- Dirección
    address_line1 VARCHAR(300),
    address_line2 VARCHAR(300),
    city VARCHAR(100) DEFAULT 'Drogheda',
    county VARCHAR(100) DEFAULT 'Louth',
    eircode VARCHAR(10),
    country VARCHAR(100) DEFAULT 'Ireland',
    
    -- Coordenadas para delivery
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8),
    
    -- Metadata
    notes TEXT,
    is_active BOOLEAN DEFAULT true,
    total_orders INTEGER DEFAULT 0,
    total_spent DECIMAL(10, 2) DEFAULT 0.00,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para búsquedas rápidas
CREATE INDEX idx_customers_phone ON customers(phone);
CREATE INDEX idx_customers_eircode ON customers(eircode);
CREATE INDEX idx_customers_name ON customers(name);

-- Datos de ejemplo
INSERT INTO customers (phone, name, email, address_line1, city, eircode) VALUES
('0871234567', 'John Doe', 'john@example.com', '123 Main Street', 'Drogheda', 'A92 X7Y8'),
('0879876543', 'Jane Smith', 'jane@example.com', '45 High Street', 'Drogheda', 'A92 K3L9')
ON CONFLICT (phone) DO NOTHING;

