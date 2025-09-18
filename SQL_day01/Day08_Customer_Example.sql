-- Create the company_db database
-- Run the following command at the TERMINAL prompt to create
-- the database and all of the objects and data inside the db
-- sqlite3 customer_db.db < Day08_Customer_Example.sql

-- Create the customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    email TEXT,
    phone TEXT
);

-- Create the orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date DATE,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Create the products table
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    unit_price REAL
);

-- Create the order_items table (Many-to-Many)
CREATE TABLE IF NOT EXISTS order_items (
    order_id INTEGER,
    product_id INTEGER,
    quantity INTEGER,
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id),
    PRIMARY KEY (order_id, product_id)
);

-- Create the addresses table
CREATE TABLE IF NOT EXISTS addresses (
    address_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    street_address TEXT,
    city TEXT,
    state TEXT,
    postal_code TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
);

-- Insert sample data (You can add more data as needed)
INSERT INTO customers (first_name, last_name, email, phone) VALUES
    ('John', 'Doe', 'john@example.com', '123-456-7890'),
    ('Jane', 'Smith', 'jane@example.com', '987-654-3210');

INSERT INTO orders (customer_id, order_date, total_amount) VALUES
    (1, '2023-01-15', 100.50),
    (2, '2023-02-20', 75.20);

INSERT INTO products (product_name, unit_price) VALUES
    ('Product A', 25.00),
    ('Product B', 30.50);

INSERT INTO order_items (order_id, product_id, quantity) VALUES
    (1, 1, 2),
    (1, 2, 3),
    (2, 1, 1);

INSERT INTO addresses (customer_id, street_address, city, state, postal_code) VALUES
    (1, '123 Main St', 'Cityville', 'CA', '12345'),
    (2, '456 Elm St', 'Townsville', 'NY', '54321');
