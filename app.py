import json
from flask import Flask, request, jsonify
import os
import sqlite3

app = Flask(__name__)

app.config['DB_PATH'] = 'shop.db'
DB_PATH = app.config['DB_PATH']


def get_db():
    db_path = app.config.get('DB_PATH', 'shop.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    db_path = app.config.get('DB_PATH', 'shop.db')
    
    if os.path.exists(db_path):
        print(f"База данных {db_path} уже существует")
    else:
        print(f"Создаётся новая база данных {db_path}")
    
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, name TEXT)''')
        cursor.execute(''' CREATE TABLE IF NOT EXISTS categories (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           parent_id INTEGER,
                           FOREIGN KEY (parent_id) REFERENCES categories(id)
                           )''')
        cursor.execute(''' CREATE TABLE IF NOT EXISTS items (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL,
                           image TEXT,
                           quantity INTEGER NOT NULL,
                           price REAL NOT NULL,
                           category_id INTEGER NOT NULL,
                           FOREIGN KEY (category_id) REFERENCES categories(id)
                           )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE NOT NULL,
                        password TEXT NOT NULL,
                        email TEXT UNIQUE NOT NULL
                    )''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS baskets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        customer_id INTEGER NOT NULL,
                        item_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        FOREIGN KEY (customer_id) REFERENCES customers(id),
                        FOREIGN KEY (item_id) REFERENCES items(id)
                    )''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Ошибка при инициализации базы данных: {e}")
    finally:
        conn.close()

def query_db(query, args=(), one=False):
    "Функция для выполнения SQL-запросов."
    conn = get_db()
    try:
        cur = conn.cursor()
        cur.execute(query, args)
        rv = cur.fetchall()
        conn.commit()
        return (rv[0] if rv else None) if one else rv
    finally:
        conn.close()

app = Flask(__name__)
# Хранение данных в памяти
categories = [] 
items = []     
customers = []
baskets = {}
# Уникальные идентификаторы
category_id_counter = 1
item_id_counter = 1

customer_id = 1

# Создание категории
@app.route('/category', methods=['POST'])
def create_category():
    global category_id_counter
    data = request.json
    name = data.get('name')
    parent_id = data.get('parent_id', None)  

    if not name:
        return jsonify({'error': 'Name is required'}), 400

    ### Проверка родителскую категрию
    if parent_id:
        parent = query_db('SELECT id FROM categories WHERE id = ?', [parent_id], one=True)
        if not parent:
            return jsonify({'error': 'Parent category does not exist'}), 400

    query_db('INSERT INTO categories (name, parent_id) VALUES (?, ?)', (name, parent_id))
    category = query_db('SELECT * FROM categories ORDER BY id DESC LIMIT 1', one=True)
    
    return jsonify({
        'message': 'Category created successfully',
        'category': dict(category)
    }), 201

# Получение всех категорий
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = query_db('SELECT * FROM categories')
    categories_list = [dict(category) for category in categories]
    return jsonify(categories_list), 200

# Добавление товара
@app.route('/items', methods=['POST'])
def add_item():
    data = request.json
    
    # Проверка обязательных полей
    required_fields = ['name', 'quantity', 'price', 'category_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Проверка существования категории
    category = query_db('SELECT id FROM categories WHERE id = ?', [data['category_id']], one=True)
    if not category:
        return jsonify({'error': 'Category does not exist'}), 404
    
    # Создание нового товара
    query_db('''
    INSERT INTO items (name, image, quantity, price, category_id)
    VALUES (?, ?, ?, ?, ?)
    ''', (data['name'], data.get('image', ''), data['quantity'], data['price'], data['category_id']))
    item = query_db("SELECT * FROM items ORDER BY id DESC LIMIT 1", one=True)
    
    return jsonify({'message': 'Item added successfully', 'item': dict(item)}), 201


# Фильтрация товаров
@app.route('/items', methods=['GET'])
def filter_items():
    keyword = request.args.get('keyword', '').lower()
    items = query_db("SELECT * FROM items WHERE LOWER(name) LIKE ?", [f'%{keyword}%'])
    return jsonify([dict(item) for item in items])


##############################################################


#Счетчик ID



# Функцияя фильтрации товаров по ключевому слову
@app.route('/items/search', methods=['GET'])

def search_items():
    keyword = request.args.get('keyword', '').lower()
    filtered_items = [item for item in items if keyword in item['name'].lower()]
    return jsonify(filtered_items)


# Создание учетной записи покупателя
@app.route('/customers', methods=['POST'])
def create_customer():
    data = request.json
    
    required_fields = ['username', 'password', 'email']

    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Проверка уникальности username
    if query_db('SELECT id FROM customers WHERE username = ?', [data['username']], one=True):
        return jsonify({'error': 'Username already exists'}), 400
    if query_db("SELECT id FROM customers WHERE email = ?", [data['email']], one=True):
        return jsonify({'error': 'Email already exists'}), 400
    
    password = data['password']
    query_db('INSERT INTO customers (username, password, email) VALUES (?, ?, ?)', [data['username'], password,data['email']])

    customer = query_db('SELECT * FROM customers ORDER BY id DESC LIMIT 1', one=True)
    return jsonify({'message': 'Customer created successfully', 'customer': dict(customer)}), 201


# Получение списка покупателей
@app.route('/customers', methods=['GET'])
def get_customers():
    customers = query_db('SELECT * FROM customers')
    return jsonify([dict(customer) for customer in customers]), 200



# Добавление товара в корзину
@app.route('/customers/<int:customer_id>/basket', methods=['POST'])
def add_to_basket(customer_id):
    data = request.json
    
    if 'item_id' not in data or 'quantity' not in data:
        return jsonify({'error': 'Missing item_id or quantity'}), 400
    
    # Проверка покупателя
    customer = query_db('SELECT id FROM customers WHERE id = ?', [customer_id], one=True)
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404
    
    # Проверка товара
    item = query_db('SELECT * FROM items WHERE id = ?', [data['item_id']], one=True)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    if item['quantity'] < data['quantity']:
        return jsonify({'error': 'Not enough items in stock'}), 400
    
    # Добавление в корзину
    query_db('''
    INSERT INTO baskets (customer_id, item_id, quantity)
    VALUES (?, ?, ?)
    ''', [customer_id, data['item_id'], data['quantity']])
    
    return jsonify({'message': 'Item added to basket successfully'}), 200

# Получение корзины покупателя
@app.route('/customers/<int:customer_id>/basket', methods=['GET'])
def get_basket(customer_id):
    basket_items = query_db('''
    SELECT b.id, i.name, i.price, b.quantity 
    FROM baskets b
    JOIN items i ON b.item_id = i.id
    WHERE b.customer_id = ?
    ''', [customer_id])
    
    return jsonify([dict(item) for item in basket_items]), 200

# Отчет по товарам и корзинам
@app.route('/report', methods=['GET'])
def generate_report():
    # Все товары
    available_items = query_db('SELECT * FROM items')
    
    # Корзины всех пользователей
    customers_baskets = []
    customers = query_db('SELECT * FROM customers')
    
    for customer in customers:
        basket = query_db('''
        SELECT i.name, i.price, b.quantity
        FROM baskets b
        JOIN items i ON b.item_id = i.id
        WHERE b.customer_id = ?
        ''', [customer['id']])
        
        total = sum(float(item['price']) * int(item['quantity']) for item in basket)
        
        customers_baskets.append({
            'customer_id': customer['id'],
            'username': customer['username'],
            'basket': [dict(item) for item in basket],
            'total': total
        })
    
    return jsonify({
        'available_items': [dict(item) for item in available_items],
        'customers_baskets': customers_baskets
    })

#Воспомогательные маршруты  для тестирования

@app.route('/')
def home():
    return """
    <h1>Интернет-магазин API</h1>
    <p>Доступные эндпоинты:</p>
    <ul>
        <li>POST /customers - Создать аккаунт покупателя</li>
        <li>POST /customers/&lt;id&gt;/basket - Добавить товар в корзину</li>
        <li>GET /items/search?keyword=... - Поиск товаров</li>
        <li>GET /report - Отчет по товарам и корзинам</li>
        <li>POST /items - Добавить товар (для теста)</li>
    </ul>
    """


if __name__ == '__main__':
    init_db()  # ← Важная строка! Создаёт таблицы при первом запуске
    app.run(debug=True)