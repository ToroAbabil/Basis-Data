CREATE DATABASE toko
    DEFAULT CHARACTER SET = 'utf8mb4';

USE toko

CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    birthdate DATE COMMENT 'Tanggal lahir pelanggan'
);

INSERT INTO customers (name, email, phone, address, birthdate) VALUES
('Egy Maulana Vikri', 'egy@gmail.com', '081234567890', 'Medan, Sumatera Utara', '2000-07-07'),
('Witan Sulaeman', 'witan@gmail.com', '081298765432', 'Palu, Sulawesi Tengah', '2001-10-08'),
('Marselino Ferdinan', 'marselino@gmail.com', '081355566677', 'Jakarta', '2004-09-09'),
('Pratama Arhan', 'arhan@gmail.com', '081223344556', 'Blora, Jawa Tengah', '2001-12-21'),
('Rizky Ridho', 'ridho@gmail.com', '081334455667', 'Surabaya, Jawa Timur', '2001-11-22');


CREATE TABLE IF NOT EXISTS products (
    product_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    stock INT NOT NULL
);

INSERT INTO products (name, description, price, stock) VALUES
('Sepatu Bola Nike', 'Sepatu bola profesional seri terbaru', 899000, 20),
('Jersey Timnas Home', 'Jersey official home 2024', 499000, 50),
('Jersey Timnas Away', 'Jersey official away 2024', 499000, 45),
('Bola Adidas', 'Bola match resmi FIFA Quality Pro', 750000, 30),
('Shin Guard', 'Pelindung tulang kering premium', 150000, 60);


CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
        ON DELETE CASCADE
);

INSERT INTO orders (customer_id, total_amount) VALUES
(1, 1398000),
(2, 998000),
(3, 1249000),
(4, 499000),
(5, 1650000);


CREATE TABLE IF NOT EXISTS order_details (
    order_detail_id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) AS (quantity * price) STORED,
    FOREIGN KEY (order_id) REFERENCES orders(order_id)
        ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(product_id)
        ON DELETE CASCADE
);

-- Order details untuk order 1–5
INSERT INTO order_details (order_id, product_id, quantity, price) VALUES
(1, 1, 1, 899000),
(1, 2, 1, 499000),

(2, 4, 1, 750000),
(2, 5, 1, 150000),
(2, 5, 1, 98000),

(3, 3, 1, 499000),
(3, 1, 1, 899000),

(4, 2, 1, 499000),

(5, 1, 1, 899000),
(5, 4, 1, 750000);

