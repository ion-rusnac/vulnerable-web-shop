-- schema.sql
-- SQLite3 database schema for the toy web shop
-- Usage:  sqlite3 shop.db < schema.sql

PRAGMA foreign_keys = ON;

-- ─── Customers ───────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS customers (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name  TEXT    NOT NULL,
    last_name   TEXT    NOT NULL,
    email       TEXT    NOT NULL UNIQUE,
    password    TEXT    NOT NULL,
    phone       TEXT,
    address     TEXT,
    city        TEXT,
    country     TEXT    DEFAULT 'US',
    balance     REAL    NOT NULL DEFAULT 0.0 CHECK (balance >= 0),
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- ─── Products ────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS products (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    description TEXT,
    price       REAL    NOT NULL CHECK (price >= 0),
    image       TEXT,
    alt         TEXT,
    badge       TEXT,                       -- e.g. 'Hot', 'New', 'Limited'
    badge_color TEXT,                       -- Bootstrap bg- class
    rating      INTEGER DEFAULT 0 CHECK (rating BETWEEN 0 AND 5),
    stock       INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    created_at  TEXT    NOT NULL DEFAULT (datetime('now'))
);

-- ─── Orders ──────────────────────────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS orders (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    status      TEXT    NOT NULL DEFAULT 'pending'
                        CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled')),
    total       REAL    NOT NULL DEFAULT 0 CHECK (total >= 0),
    created_at  TEXT    NOT NULL DEFAULT (datetime('now')),
    updated_at  TEXT    NOT NULL DEFAULT (datetime('now')),

    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

-- ─── Order Items (junction table between orders and products) ────────────────

CREATE TABLE IF NOT EXISTS order_items (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id    INTEGER NOT NULL,
    product_id  INTEGER NOT NULL,
    quantity    INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0),
    unit_price  REAL    NOT NULL CHECK (unit_price >= 0),

    FOREIGN KEY (order_id)   REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

-- ─── Indexes ─────────────────────────────────────────────────────────────────

CREATE INDEX IF NOT EXISTS idx_orders_customer   ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_order_items_order  ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_customers_email    ON customers(email);

-- ─── Seed data (mirrors the existing product catalogue in app.py) ────────────

INSERT INTO products (name, price, image, alt, badge, badge_color, rating, stock) VALUES
    ('Articulated Dragon',  35.00, 'https://images.unsplash.com/photo-1593305841991-05c297ba4575?auto=format&fit=crop&q=80&w=450&h=300', 'Articulated Crystal Dragon', NULL,      NULL,         0, 20),
    ('Flexi Octopus',       15.00, 'https://images.unsplash.com/photo-1558060370-d644479cb6f7?auto=format&fit=crop&q=80&w=450&h=300',  'Flexi Octopus',              'Hot',     'bg-primary', 5, 50),
    ('Low-Poly T-Rex',      22.00, 'https://images.unsplash.com/photo-1532330393533-443990a51d10?auto=format&fit=crop&q=80&w=450&h=300', 'Low-Poly T-Rex',             NULL,      NULL,         0, 30),
    ('Custom D&D Mini',     45.00, 'https://images.unsplash.com/photo-1612036782180-6f0b6cd846fe?auto=format&fit=crop&q=80&w=450&h=300', 'Custom D&D Mini',            NULL,      NULL,         5, 10),
    ('Robot Explorer',      28.00, 'https://images.unsplash.com/photo-1566131444841-9442f360c704?auto=format&fit=crop&q=80&w=450&h=300', 'Robot Action Figure',         'New',     'bg-dark',    0, 25),
    ('Puzzle Cube',         18.00, 'https://images.unsplash.com/photo-1587654538522-6bcd2483b1db?auto=format&fit=crop&q=80&w=450&h=300', 'Puzzle Cube',                NULL,      NULL,         0, 40),
    ('Spaceship Model',     55.00, 'https://images.unsplash.com/photo-1446776811953-b23d57bd21aa?auto=format&fit=crop&q=80&w=450&h=300', 'Spaceship Model',            'Limited', 'bg-primary', 5,  5),
    ('Medieval Castle',     75.00, 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&q=80&w=450&h=300',    'Medieval Castle Set',         NULL,      NULL,         0, 15);

-- Sample customer
INSERT INTO customers (first_name, last_name, email, password, phone, address, city, country) VALUES
    ('Alice', 'Johnson', 'alice@example.com', 'changeme123', '+1-555-0100', '123 Maple St', 'Springfield', 'US');

-- Sample order for Alice
INSERT INTO orders (customer_id, status, total) VALUES
    (1, 'pending', 50.00);

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
    (1, 1, 1, 35.00),
    (1, 2, 1, 15.00);
