from app import app, get_db
import requests
import sqlite3

BASE_URL = "http://127.0.0.1:5000"

def test_create_category():
    test_data = {
        'name': 'оДЕЖДА',
        'parent_id': None 
    }
    response = requests.post(f"{BASE_URL}/category", json=test_data)

    assert response.status_code == 201
    assert response.json()['category']['name'] == 'оДЕЖДА'

def test_get_categories():
    response = requests.get(f"{BASE_URL}/categories")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_item():
    test_category = {'name': 'Test-category'}
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM categories WHERE name = ?", (test_category['name'],))
        category = cursor.fetchone()
        
        if not category:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (test_category['name'],))
            conn.commit()
            category_id = cursor.lastrowid
        else:
            category_id = category['id']
        conn.close()

    test_data = {
        'name': 'Футболка', 
        'quantity': 10, 
        'price': "10200", 
        'category_id': category_id
    }
    
    response = requests.post(f"{BASE_URL}/items", json=test_data)
    assert response.status_code in [201, 400, 404]
    
    # Проверяем запись в БД
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM items WHERE name = ?", (test_data['name'],))
        result = cursor.fetchone()
        conn.close()
        assert result is not None, "Item was not added to DB"

def test_filter_items():
    response = requests.get(f"{BASE_URL}/items?keyword=TestItem")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    if items:
        assert 'TestItem' in items[0]['name']

def test_search_items():
    response = requests.get(f"{BASE_URL}/items/search?keyword=TestItem")
    assert response.status_code == 200
    items = response.json()
    assert isinstance(items, list)
    if items:
        assert 'TestItem' in items[0]['name']


def test_get_customers():
    response = requests.get(f"{BASE_URL}/customers")
    assert response.status_code == 200
    customers = response.json()
    assert isinstance(customers, list)
    if customers:
        assert any(c['username'] == 'testuser' for c in customers)

def test_get_basket():
    # Получаем ID тестового пользователя
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM customers WHERE username = 'testuser'")
        customer = cursor.fetchone()
        conn.close()
        
        if customer:
            response = requests.get(f"{BASE_URL}/customers/{customer['id']}/basket")
            assert response.status_code == 200
            basket = response.json()
            assert isinstance(basket, list)
            if basket:
                assert basket[0]['name'] == 'TestItem'

def test_generate_report():
    response = requests.get(f"{BASE_URL}/report")
    assert response.status_code == 200
    report = response.json()
    assert isinstance(report, dict)
    assert 'available_items' in report
    assert 'customers_baskets' in report

if __name__ == "__main__":
    # Запуск тестов
    test_get_categories()
    test_add_item()
    test_filter_items()
    test_search_items()
    test_get_customers()
    test_get_basket()
    test_generate_report()
    print("All tests passed!")
