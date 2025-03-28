import pytest
from app import app

def test_create_category():
    client = app.test_client()
    response = client.post('/category', json={'name': 'transport'})
    assert response.status_code == 201
    assert response.json['category']['name'] == 'transport'

def test_get_categories():
    client = app.test_client()
    response = client.get('/categories')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_add_item():
    client = app.test_client()
    # Создаем категорию для теста
    client.post('/category', json={'name': 'Books'})
    response = client.post('/items', json={'name': 'Python Book', 'quantity': 10, 'price': 25, 'category_id': 1})
    assert response.status_code == 201
    assert response.json['item']['name'] == 'Python Book'

def test_search_items():
    client = app.test_client()
    response = client.get('/items/search?keyword=Python')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_create_customer():
    client = app.test_client()
    response = client.post('/customers', json={'username': 'nuras', 'password': '1234', 'email': 'nuras@gmail.com'})
    assert response.status_code == 201
    assert response.json['customer']['username'] == 'nuras'

def test_get_customers():
    client = app.test_client()
    response = client.get('/customers')
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_add_to_basket():
    client = app.test_client()
    # Создаем пользователя
    client.post('/customers', json={'username': 'yerzhan', 'password': '123', 'email': 'ers@gmail.com'})
    # Создаем категорию и товар
    client.post('/category', json={'name': 'Shoes'})
    client.post('/items', json={'name': 'shoes adidas', 'quantity': 5, 'price': 25.000, 'category_id': 2})
    # Добавляем товар в корзину
    response = client.post('/customers/2/basket', json={'item_id': 2, 'quantity': 1})
    assert response.status_code == 200

def test_generate_report():
    client = app.test_client()
    response = client.get('/report')
    assert response.status_code == 200
    assert 'available_items' in response.json
