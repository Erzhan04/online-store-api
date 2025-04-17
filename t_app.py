# from app import app, get_db
# import requests

# BASE_URL = "http://127.0.0.1:5000"

# def test_get_categories():
#     response = requests.get(f"{BASE_URL}/categories")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_add_item():
#     test_data = {'name': 'Shoes', 'quantity': 10, 'price': "1000", 'category_id': 1}
#     response = requests.post(f"{BASE_URL}/items", json=test_data)
#     assert response.status_code in [201, 400, 404]

# def test_filter_items():
#     response = requests.get(f"{BASE_URL}/items?keyword=Shoes")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_search_items():
#     response = requests.get(f"{BASE_URL}/items/search?keyword=Shoes")
#     if response == []:
#         print('Null')
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_create_customer():
#     test_data = {'username': 'testuwwwwwwwwser', 'password': '1234', 'email': 'test@example.com'}
#     response = requests.post(f"{BASE_URL}/customers", json=test_data)
#     assert response.status_code in [201, 400]

# def test_get_customers():
#     response = requests.get(f"{BASE_URL}/customers")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_add_to_basket():
#     test_data = {'item_id': 1, 'quantity': 2}
#     response = requests.post(f"{BASE_URL}/customers/1/basket", json=test_data)
#     assert response.status_code in [200, 400, 404]

# def test_get_basket():
#     response = requests.get(f"{BASE_URL}/customers/1/basket")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_generate_report():
#     response = requests.get(f"{BASE_URL}/report")
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)

# if __name__ == "__main__":
#     test_get_categories()
#     test_add_item()
#     test_filter_items()
#     test_search_items()
#     test_create_customer()
#     test_get_customers()
#     test_add_to_basket()
#     test_get_basket()
#     test_generate_report()
#     print("All tests passed!")





























# from app import app, get_db
# import requests
# import sqlite3
# import pytest

# @pytest.fixture
# def client():
#     with app.test_client() as client:
#         yield client


# BASE_URL = "http://127.0.0.1:5000"




# def test_get_categories():
#     response = requests.get(f"{BASE_URL}/categories")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_add_item():
#     # Получаем первую категорию из БД для теста
#     with app.app_context():
#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute("SELECT id FROM categories LIMIT 1")
#         category = cursor.fetchone()
#         conn.close()
        
#         if category:
#             test_data = {'name': 'Test Item', 'quantity': 5, 'price': "100", 'category_id': category['id']}
#             response = requests.post(f"{BASE_URL}/items", json=test_data)
#             assert response.status_code in [201, 400, 404]

# def test_filter_items():
#     response = requests.get(f"{BASE_URL}/items?keyword=Test")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_search_items():
#     response = requests.get(f"{BASE_URL}/items/search?keyword=Test")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_create_customer():
#     test_data = {'username': 'testuser', 'password': 'testpass', 'email': 'test@example.com'}
#     response = requests.post(f"{BASE_URL}/customers", json=test_data)
#     assert response.status_code in [201, 400]

# def test_get_customers():
#     response = requests.get(f"{BASE_URL}/customers")
#     assert response.status_code == 200
#     assert isinstance(response.json(), list)

# def test_add_to_basket():
#     # Получаем первого пользователя и товар из БД для теста
#     with app.app_context():
#         conn = get_db()
#         cursor = conn.cursor()
        
#         cursor.execute("SELECT id FROM customers LIMIT 1")
#         customer = cursor.fetchone()
        
#         cursor.execute("SELECT id FROM items LIMIT 1")
#         item = cursor.fetchone()
        
#         conn.close()
        
#         if customer and item:
#             test_data = {'item_id': item['id'], 'quantity': 1}
#             response = requests.post(f"{BASE_URL}/customers/{customer['id']}/basket", json=test_data)
#             assert response.status_code in [200, 400, 404]

# def test_get_basket():
#     # Получаем первого пользователя из БД для теста
#     with app.app_context():
#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute("SELECT id FROM customers LIMIT 1")
#         customer = cursor.fetchone()
#         conn.close()
        
#         if customer:
#             response = requests.get(f"{BASE_URL}/customers/{customer['id']}/basket")
#             assert response.status_code == 200
#             assert isinstance(response.json(), list)

# def test_generate_report():
#     response = requests.get(f"{BASE_URL}/report")
#     assert response.status_code == 200
#     assert isinstance(response.json(), dict)

# if __name__ == "__main__":
#     # Запуск тестов
#     test_get_categories()
#     test_add_item()
#     test_filter_items()
#     test_search_items()
#     test_create_customer()
#     test_get_customers()
#     test_add_to_basket()
#     test_get_basket()
#     test_generate_report()
#     print("All tests passed!")






























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

# def test_create_customer():
#     test_data = {
#         'username': 'yerzhan', 
#         'password': 'qweasd', 
#         'email': 'ye@example.com'
#     }
    
#     with app.app_context():
#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute("SELECT id FROM customers WHERE username = ?", (test_data['username'],))
#         assert cursor.fetchone() is None, "Test user already exists in DB"
#         conn.close()
    
#     response = requests.post(f"{BASE_URL}/customers", json=test_data)
#     assert response.status_code in [201, 400]
    
#     with app.app_context():
#         conn = get_db()
#         cursor = conn.cursor()
#         cursor.execute("SELECT username FROM customers WHERE username = ?", (test_data['username'],))
#         result = cursor.fetchone()
#         conn.close()
#         assert result is not None, "Customer was not added to DB"

def test_get_customers():
    response = requests.get(f"{BASE_URL}/customers")
    assert response.status_code == 200
    customers = response.json()
    assert isinstance(customers, list)
    if customers:
        assert any(c['username'] == 'testuser' for c in customers)

# def test_add_to_basket():
#     # Получаем ID тестового пользователя и товара
#     with app.app_context():
#         conn = get_db()
#         cursor = conn.cursor()
        
#         cursor.execute("SELECT id FROM customers WHERE username = 'testuser'")
#         customer = cursor.fetchone()
        
#         cursor.execute("SELECT id FROM items WHERE name = 'TestItem'")
#         item = cursor.fetchone()
        
#         conn.close()
        
#         if customer and item:
#             test_data = {'item_id': item['id'], 'quantity': 1}
#             response = requests.post(
#                 f"{BASE_URL}/customers/{customer['id']}/basket", 
#                 json=test_data
#             )
#             assert response.status_code in [200, 400, 404]
            
#             # Проверяем запись в БД
#             conn = get_db()
#             cursor = conn.cursor()
#             cursor.execute(
#                 "SELECT id FROM baskets WHERE customer_id = ? AND item_id = ?",
#                 (customer['id'], item['id'])
#             )
#             result = cursor.fetchone()
#             conn.close()
#             assert result is not None, "Item was not added to basket"

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
    test_create_customer()
    test_get_customers()
    test_add_to_basket()
    test_get_basket()
    test_generate_report()
    print("All tests passed!")
