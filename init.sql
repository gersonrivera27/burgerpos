-- Tabla de Categorías
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Productos
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id),
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(500),
    is_available BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Extras/Modificadores
CREATE TABLE modifiers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) DEFAULT 0.00,
    modifier_type VARCHAR(50), -- 'extra', 'remove', 'substitute'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Mesas (opcional)
CREATE TABLE tables (
    id SERIAL PRIMARY KEY,
    table_number INTEGER UNIQUE NOT NULL,
    capacity INTEGER,
    status VARCHAR(20) DEFAULT 'available', -- 'available', 'occupied', 'reserved'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Órdenes
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    table_id INTEGER REFERENCES tables(id),
    order_number VARCHAR(50) UNIQUE NOT NULL,
    customer_name VARCHAR(200),
    order_type VARCHAR(20) NOT NULL, -- 'dine-in', 'takeout', 'delivery'
    status VARCHAR(20) DEFAULT 'pending', -- 'pending', 'preparing', 'ready', 'completed', 'cancelled'
    subtotal DECIMAL(10, 2) NOT NULL,
    tax DECIMAL(10, 2) DEFAULT 0.00,
    discount DECIMAL(10, 2) DEFAULT 0.00,
    total DECIMAL(10, 2) NOT NULL,
    payment_method VARCHAR(50), -- 'cash', 'card', 'transfer'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Tabla de Items de Orden
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL DEFAULT 1,
    unit_price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    special_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de Modificadores por Item
CREATE TABLE order_item_modifiers (
    id SERIAL PRIMARY KEY,
    order_item_id INTEGER REFERENCES order_items(id) ON DELETE CASCADE,
    modifier_id INTEGER REFERENCES modifiers(id),
    quantity INTEGER DEFAULT 1,
    price DECIMAL(10, 2) NOT NULL
);

-- Tabla de Usuarios (cajeros/empleados)
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(200) NOT NULL,
    role VARCHAR(50) NOT NULL, -- 'admin', 'cashier', 'kitchen'
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Índices para mejor rendimiento
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);

-- Datos de ejemplo
INSERT INTO categories (name, description) VALUES 
    ('Hamburguesas', 'Hamburguesas clásicas y especiales'),
    ('Bebidas', 'Refrescos, jugos y más'),
    ('Extras', 'Papas, aros de cebolla, etc'),
    ('Postres', 'Helados y dulces');

INSERT INTO products (category_id, name, description, price) VALUES 
    (1, 'Hamburguesa Clásica', 'Carne, lechuga, tomate, cebolla', 8.99),
    (1, 'Hamburguesa Doble', 'Doble carne con queso', 12.99),
    (1, 'Hamburguesa BBQ', 'Carne, queso, tocino, salsa BBQ', 11.99),
    (2, 'Coca Cola', 'Refresco 500ml', 2.50),
    (2, 'Agua', 'Agua natural 500ml', 1.50),
    (3, 'Papas Fritas', 'Porción grande', 3.99),
    (3, 'Aros de Cebolla', 'Porción mediana', 4.50);

INSERT INTO modifiers (name, price, modifier_type) VALUES 
    ('Queso extra', 1.00, 'extra'),
    ('Tocino', 1.50, 'extra'),
    ('Sin cebolla', 0.00, 'remove'),
    ('Sin tomate', 0.00, 'remove'),
    ('Aguacate', 2.00, 'extra');