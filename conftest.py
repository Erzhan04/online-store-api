import pytest
import sqlite3
from app import app, get_db

TEST_DB = "test.db"

@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["DATABASE"] = TEST_DB

    with app.test_client() as client:
        with app.app_context():
            init_test_db()  # Создание тестовой БД
        yield client

    # Удаляем тестовую БД после завершения тестов
    import os
    os.remove(TEST_DB)

def init_test_db():
    """Создаёт тестовую базу данных."""
    conn = sqlite3.connect(TEST_DB)
    cursor = conn.cursor()

    # Создаём таблицы
    cursor.executescript("""
    DROP TABLE IF EXISTS categories;
    DROP TABLE IF EXISTS items;
    DROP TABLE IF EXISTS customers;
    DROP TABLE IF EXISTS baskets;

    CREATE TABLE categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );

    CREATE TABLE items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        image TEXT,
        quantity INTEGER NOT NULL,
        price REAL NOT NULL,
        category_id INTEGER NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    );

    CREATE TABLE customers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    );

    CREATE TABLE baskets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_id INTEGER NOT NULL,
        item_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (customer_id) REFERENCES customers (id),
        FOREIGN KEY (item_id) REFERENCES items (id)
    );
    """)
    conn.commit()
    conn.close()
