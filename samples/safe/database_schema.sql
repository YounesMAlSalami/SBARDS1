-- Database Schema for E-Commerce Application
-- Version: 1.0.0
-- Date: 2025-05-15
-- Author: Database Team

-- This is a safe SQL file with no malicious content
-- It contains a standard database schema for an e-commerce application

-- Drop tables if they exist (for clean installation)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS product_reviews;
DROP TABLE IF EXISTS product_categories;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS user_addresses;
DROP TABLE IF EXISTS user_payment_methods;
DROP TABLE IF EXISTS user_sessions;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS countries;

-- Create tables

-- Countries table
CREATE TABLE countries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Users table
CREATE TABLE users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    phone VARCHAR(20),
    is_admin BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    email_verified BOOLEAN DEFAULT FALSE,
    email_verification_token VARCHAR(100),
    password_reset_token VARCHAR(100),
    password_reset_expires DATETIME,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login DATETIME,
    INDEX idx_email (email),
    INDEX idx_is_active (is_active)
);

-- User sessions table
CREATE TABLE user_sessions (
    id VARCHAR(100) PRIMARY KEY,
    user_id INT NOT NULL,
    ip_address VARCHAR(45) NOT NULL,
    user_agent VARCHAR(255),
    expires_at DATETIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- User payment methods table
CREATE TABLE user_payment_methods (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    payment_type ENUM('credit_card', 'paypal', 'bank_transfer') NOT NULL,
    provider VARCHAR(50) NOT NULL,
    account_number_last4 VARCHAR(4),
    expiry_date VARCHAR(7),
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- User addresses table
CREATE TABLE user_addresses (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    address_line1 VARCHAR(100) NOT NULL,
    address_line2 VARCHAR(100),
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50),
    postal_code VARCHAR(20) NOT NULL,
    country_id INT NOT NULL,
    is_default_shipping BOOLEAN DEFAULT FALSE,
    is_default_billing BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (country_id) REFERENCES countries(id)
);

-- Categories table
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    parent_id INT,
    slug VARCHAR(50) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL,
    INDEX idx_slug (slug),
    INDEX idx_is_active (is_active)
);

-- Products table
CREATE TABLE products (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    sku VARCHAR(50) NOT NULL UNIQUE,
    price DECIMAL(10, 2) NOT NULL,
    sale_price DECIMAL(10, 2),
    stock_quantity INT NOT NULL DEFAULT 0,
    weight DECIMAL(8, 2),
    dimensions VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    is_featured BOOLEAN DEFAULT FALSE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    meta_title VARCHAR(100),
    meta_description VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_sku (sku),
    INDEX idx_slug (slug),
    INDEX idx_is_active (is_active),
    INDEX idx_is_featured (is_featured)
);

-- Product categories table (many-to-many relationship)
CREATE TABLE product_categories (
    product_id INT NOT NULL,
    category_id INT NOT NULL,
    PRIMARY KEY (product_id, category_id),
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
);

-- Product reviews table
CREATE TABLE product_reviews (
    id INT PRIMARY KEY AUTO_INCREMENT,
    product_id INT NOT NULL,
    user_id INT NOT NULL,
    rating TINYINT NOT NULL CHECK (rating BETWEEN 1 AND 5),
    title VARCHAR(100),
    review TEXT,
    is_approved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id),
    INDEX idx_user_id (user_id),
    INDEX idx_is_approved (is_approved)
);

-- Orders table
CREATE TABLE orders (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    order_number VARCHAR(20) NOT NULL UNIQUE,
    status ENUM('pending', 'processing', 'shipped', 'delivered', 'cancelled') NOT NULL DEFAULT 'pending',
    total_amount DECIMAL(10, 2) NOT NULL,
    tax_amount DECIMAL(10, 2) NOT NULL,
    shipping_amount DECIMAL(10, 2) NOT NULL,
    discount_amount DECIMAL(10, 2) NOT NULL DEFAULT 0,
    shipping_address_id INT NOT NULL,
    billing_address_id INT NOT NULL,
    payment_method_id INT NOT NULL,
    shipping_method VARCHAR(50) NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (shipping_address_id) REFERENCES user_addresses(id),
    FOREIGN KEY (billing_address_id) REFERENCES user_addresses(id),
    FOREIGN KEY (payment_method_id) REFERENCES user_payment_methods(id),
    INDEX idx_order_number (order_number),
    INDEX idx_status (status),
    INDEX idx_user_id (user_id)
);

-- Order items table
CREATE TABLE order_items (
    id INT PRIMARY KEY AUTO_INCREMENT,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10, 2) NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id),
    INDEX idx_product_id (product_id)
);

-- Insert sample data

-- Insert countries
INSERT INTO countries (name, code) VALUES 
('United States', 'US'),
('Canada', 'CA'),
('United Kingdom', 'GB'),
('Australia', 'AU'),
('Germany', 'DE'),
('France', 'FR'),
('Japan', 'JP'),
('China', 'CN'),
('Brazil', 'BR'),
('India', 'IN');

-- Insert categories
INSERT INTO categories (name, description, parent_id, slug, is_active) VALUES
('Electronics', 'Electronic devices and accessories', NULL, 'electronics', TRUE),
('Computers', 'Desktop and laptop computers', 1, 'computers', TRUE),
('Smartphones', 'Mobile phones and accessories', 1, 'smartphones', TRUE),
('Clothing', 'Apparel and fashion items', NULL, 'clothing', TRUE),
('Men''s Clothing', 'Clothing for men', 4, 'mens-clothing', TRUE),
('Women''s Clothing', 'Clothing for women', 4, 'womens-clothing', TRUE),
('Home & Kitchen', 'Home and kitchen products', NULL, 'home-kitchen', TRUE),
('Books', 'Books and publications', NULL, 'books', TRUE),
('Sports & Outdoors', 'Sports equipment and outdoor gear', NULL, 'sports-outdoors', TRUE),
('Toys & Games', 'Toys and games for all ages', NULL, 'toys-games', TRUE);

-- Create views

-- Active products view
CREATE VIEW active_products AS
SELECT p.id, p.name, p.description, p.price, p.stock_quantity, p.slug,
       GROUP_CONCAT(DISTINCT c.name ORDER BY c.name ASC SEPARATOR ', ') AS categories
FROM products p
JOIN product_categories pc ON p.id = pc.product_id
JOIN categories c ON pc.category_id = c.id
WHERE p.is_active = TRUE
GROUP BY p.id;

-- Product reviews summary view
CREATE VIEW product_reviews_summary AS
SELECT p.id AS product_id, p.name AS product_name,
       COUNT(pr.id) AS review_count,
       ROUND(AVG(pr.rating), 1) AS average_rating
FROM products p
LEFT JOIN product_reviews pr ON p.id = pr.product_id AND pr.is_approved = TRUE
GROUP BY p.id;

-- User orders summary view
CREATE VIEW user_orders_summary AS
SELECT u.id AS user_id, u.email, u.first_name, u.last_name,
       COUNT(o.id) AS order_count,
       SUM(o.total_amount) AS total_spent,
       MAX(o.created_at) AS last_order_date
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- Create stored procedures

-- Get product details with categories and reviews
DELIMITER //
CREATE PROCEDURE get_product_details(IN product_slug VARCHAR(100))
BEGIN
    SELECT p.*, 
           GROUP_CONCAT(DISTINCT c.name ORDER BY c.name ASC SEPARATOR ', ') AS categories,
           COUNT(pr.id) AS review_count,
           ROUND(AVG(pr.rating), 1) AS average_rating
    FROM products p
    LEFT JOIN product_categories pc ON p.id = pc.product_id
    LEFT JOIN categories c ON pc.category_id = c.id
    LEFT JOIN product_reviews pr ON p.id = pr.product_id AND pr.is_approved = TRUE
    WHERE p.slug = product_slug AND p.is_active = TRUE
    GROUP BY p.id;
END //
DELIMITER ;

-- Create order
DELIMITER //
CREATE PROCEDURE create_order(
    IN p_user_id INT,
    IN p_shipping_address_id INT,
    IN p_billing_address_id INT,
    IN p_payment_method_id INT,
    IN p_shipping_method VARCHAR(50),
    IN p_notes TEXT
)
BEGIN
    DECLARE order_id INT;
    DECLARE order_number VARCHAR(20);
    
    -- Generate unique order number (YYYYMMDD-XXXX format)
    SET order_number = CONCAT(
        DATE_FORMAT(NOW(), '%Y%m%d'),
        '-',
        LPAD(FLOOR(RAND() * 10000), 4, '0')
    );
    
    -- Start transaction
    START TRANSACTION;
    
    -- Insert order
    INSERT INTO orders (
        user_id, order_number, status, total_amount, tax_amount, 
        shipping_amount, shipping_address_id, billing_address_id, 
        payment_method_id, shipping_method, notes
    ) VALUES (
        p_user_id, order_number, 'pending', 0, 0, 
        0, p_shipping_address_id, p_billing_address_id, 
        p_payment_method_id, p_shipping_method, p_notes
    );
    
    -- Get the new order ID
    SET order_id = LAST_INSERT_ID();
    
    -- Commit transaction
    COMMIT;
    
    -- Return the new order ID and number
    SELECT order_id, order_number;
END //
DELIMITER ;

-- Create triggers

-- Update product stock after order
DELIMITER //
CREATE TRIGGER after_order_item_insert
AFTER INSERT ON order_items
FOR EACH ROW
BEGIN
    UPDATE products
    SET stock_quantity = stock_quantity - NEW.quantity
    WHERE id = NEW.product_id;
END //
DELIMITER ;

-- Prevent negative stock
DELIMITER //
CREATE TRIGGER before_order_item_insert
BEFORE INSERT ON order_items
FOR EACH ROW
BEGIN
    DECLARE available_stock INT;
    
    -- Get available stock
    SELECT stock_quantity INTO available_stock
    FROM products
    WHERE id = NEW.product_id;
    
    -- Check if enough stock is available
    IF available_stock < NEW.quantity THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Insufficient stock available';
    END IF;
END //
DELIMITER ;
