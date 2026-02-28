-- Wahat Al Jazzat Cafeteria - AI Receptionist Database Schema

CREATE DATABASE IF NOT EXISTS wahat_al_jazzat;
USE wahat_al_jazzat;

-- Menu Items Table
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(255) NOT NULL,
    category ENUM('BREAKFAST', 'MAIN_DISHES', 'RICE', 'BEVERAGES', 'CAKES_SNACKS') NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    preparation_time INT DEFAULT 15, -- minutes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Customer Sessions Table
CREATE TABLE IF NOT EXISTS sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    customer_name VARCHAR(255),
    phone_number VARCHAR(20),
    email VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Orders Table
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    customer_name VARCHAR(255),
    phone_number VARCHAR(20),
    order_status ENUM('pending', 'preparing', 'ready', 'completed', 'cancelled') DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    special_requests TEXT,
    delivery_method ENUM('pickup', 'delivery') DEFAULT 'pickup',
    delivery_address TEXT,
    estimated_time INT, -- minutes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

-- Order Items Table
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    item_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    special_instructions TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (item_id) REFERENCES menu_items(id) ON DELETE CASCADE
);

-- Conversation History Table
CREATE TABLE IF NOT EXISTS conversation_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(100) NOT NULL,
    role ENUM('customer', 'assistant') NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES sessions(session_id) ON DELETE CASCADE
);

-- Order Status Changes Log
CREATE TABLE IF NOT EXISTS order_status_log (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    previous_status VARCHAR(50),
    new_status VARCHAR(50) NOT NULL,
    changed_by VARCHAR(100),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE
);

-- Insert Menu Items (based on the Wahat Al Jazzat menu)
INSERT INTO menu_items (item_name, category, description, price, preparation_time) VALUES
-- Breakfast Items
('Foul Madamas', 'BREAKFAST', 'Traditional fava beans with olive oil, lemon, and spices', 2.500, 20),
('Madrooba', 'BREAKFAST', 'Slow-cooked spiced porridge', 3.000, 25),
('Balaleet', 'BREAKFAST', 'Sweet vermicelli omelet', 2.500, 15),
('Egg Dishes', 'BREAKFAST', 'Various egg preparations', 2.000, 10),

-- Main Dishes
('Chicken Machboos', 'MAIN_DISHES', 'Traditional Bahraini spiced chicken with rice', 5.500, 30),
('Grilled Chicken', 'MAIN_DISHES', 'Char-grilled chicken with herbs', 6.000, 25),
('Chicken Curry', 'MAIN_DISHES', 'Aromatic chicken curry', 5.000, 25),
('Fish Dish', 'MAIN_DISHES', 'Fresh fish preparation', 7.000, 30),

-- Rice Dishes
('White Rice', 'RICE', 'Plain steamed white rice', 1.000, 15),
('White Rice with Vermicelli', 'RICE', 'Steamed rice with toasted vermicelli', 1.500, 15),

-- Beverages
('Tea', 'BEVERAGES', 'Traditional Bahraini tea', 0.500, 5),
('Coffee', 'BEVERAGES', 'Arabic coffee', 0.750, 5),
('Karak', 'BEVERAGES', 'Strong spiced tea with milk', 0.750, 5),
('Fresh Juices', 'BEVERAGES', 'Assorted fresh fruit juices', 2.000, 5),

-- Cakes & Snacks
('Assorted Cakes', 'CAKES_SNACKS', 'Various cake selections', 2.000, 5),
('Pastries', 'CAKES_SNACKS', 'Traditional pastries', 1.500, 5),
('Snacks', 'CAKES_SNACKS', 'Assorted snacks', 1.000, 5);

-- Indexes for better performance
CREATE INDEX idx_orders_status ON orders(order_status);
CREATE INDEX idx_orders_created ON orders(created_at);
CREATE INDEX idx_conversation_session ON conversation_history(session_id);
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_menu_category ON menu_items(category);
