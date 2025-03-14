from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранение данных в памяти
categories = [] 
items = []     

# Уникальные идентификаторы
category_id_counter = 1
item_id_counter = 1

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

# Добавление товара
@app.route('/item', methods=['POST'])
def add_item():
    global item_id_counter
    data = request.json
    name = data.get('name')
    image = data.get('image')  
    quantity = data.get('quantity')
    price = data.get('price')
    category_id = data.get('category_id')

    # Проверка обязательных полей
    if not all([name, quantity, price, category_id]):
        return jsonify({'error': 'Missing required fields'}), 400

    # Проверка, что категория существует
    category_exists = any(cat['id'] == category_id for cat in categories)
    if not category_exists:
        return jsonify({'error': 'Category does not exist'}), 404

    # Создание нового товара
    new_item = {
        'id': item_id_counter,
        'name': name,
        'image': image,
        'quantity': quantity,
        'price': price,
        'category_id': category_id
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


if __name__ == '__main__':
    app.run(debug=True)