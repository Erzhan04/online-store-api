import json
from flask import Flask, request, jsonify
import os

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
    if parent_id is not None:
        parent_exists = any(cat['id'] == parent_id for cat in categories)
        if not parent_exists:
            return jsonify({'error': 'Parent category does not exist'}), 400

    # Создание новой категории
    new_category = {
        'id': category_id_counter,
        'name': name,
        'parent_id': parent_id
    }
    categories.append(new_category)
    category_id_counter += 1

    return jsonify({'message': 'Category created successfully', 'category': new_category}), 201

@app.route('/categories', methods=['GET'])
def get_categories():
    return jsonify(categories), 200

# Добавление товара
@app.route('/items', methods=['POST'])
def add_item():
    global item_id_counter
    data = request.json
    
    # Проверка обязательных полей
    required_fields = ['name', 'quantity', 'price', 'category_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Проверка существования категории
    if not any(cat['id'] == data['category_id'] for cat in categories):
        return jsonify({'error': 'Category does not exist'}), 404
    
    # Создание нового товара
    new_item = {
        'id': item_id_counter,
        'name': data['name'],
        'quantity': data['quantity'],
        'price': data['price'],
        'category_id': data['category_id'],
        'image': data.get('image', '')  # Необязательное поле
    }
    items.append(new_item)
    item_id_counter += 1
    
    return jsonify({'message': 'Item added successfully', 'item': new_item}), 201

# Фильтрация товаров
@app.route('/items', methods=['GET'])
def filter_items():
    keyword = request.args.get('keyword', '').lower()
    filtered_items = [item for item in items if keyword in item['name'].lower()]
    return jsonify(filtered_items)


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
    global customer_id
    data = request.json
    
    required_fields = ['username', 'password', 'email']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400  #
    
    # Проверка уникальности username
    if any(customer['username'] == data['username'] for customer in customers):
        return jsonify({'error': 'Username already exists'}), 400 
    
    new_customer = {
        'id': customer_id,
        'username': data['username'],
        'password': data['password'], 
        'email': data['email'],
        'basket': []
    }
    
    customers.append(new_customer)
    customer_id += 1
    
    return jsonify({'message': 'Customer created successfully', 'customer': new_customer}), 201

@app.route('/customers', methods=['GET'])
def get_customers():
    return jsonify(customers), 200


# Добавление товара в корзину (новый метод)
@app.route('/customers/<int:customer_id>/basket', methods=['POST'])
def add_to_basket(customer_id):
    data = request.json
    
    if 'item_id' not in data or 'quantity' not in data:
        return jsonify({'error': 'Missing item_id or quantity'}), 400

    # Поиск покупателя
    customer = None
    for c in customers:
        if c['id'] == customer_id:
            customer = c
            break
    if not customer:
        return jsonify({'error': 'Customer not found'}), 404

    # Поиск товара
    item = None
    for i in items:
        if i['id'] == data['item_id']:
            item = i
            break
    if not item:
        return jsonify({'error': 'Item not found'}), 404

    # Добавление в корзину
    if customer_id not in baskets:
        baskets[customer_id] = []
        
    baskets[customer_id].append({
        'item_id': data['item_id'],
        'quantity': data['quantity'],
        'name': item['name'],
        'price': item['price']
    })
    
    return jsonify({'message': 'Item added to basket successfully'}), 200



#Отчет т товарах и корзине 

@app.route('/report', methods=['GET'])
def generate_report():
    report = {
        'available_items': items,
        'customers_baskets': [
            {
                'customer_id': c['id'],
                'username': c['username'],
                'basket': baskets.get(c['id'], []),
                'total': sum(item['price'] * item['quantity'] for item in baskets.get(c['id'], []))
            }
            for c in customers
        ]
    }
    return jsonify(report)

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
    app.run(debug=True)