import pytest
from app import app, get_db
from httpx import AsyncClient, ASGITransport

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_get_categories(client):
    response = client.get('/categories')
    assert response.status_code == 200
    
    # Проверяем, что ответ содержит данные из БД
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM categories")
    db_count = cursor.fetchone()[0]
    conn.close()
    
    assert len(response.json) == db_count

def test_create_category(client):
    test_data = {'name': 'bhybhbbhb категория'}
    
    response = client.post('/category',
        json=test_data,
        headers={'Content-Type': 'application/json'}
    )
    assert response.status_code == 201
    
    # Проверяем запись в БД
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM categories WHERE name = ?", (test_data['name'],))
    result = cursor.fetchone()
    conn.close()
    
    assert result is not None
    assert result['name'] == test_data['name']


# def test_add_items(client):
#     test_data = {'name': 'T-Shirt', 'quantity': 13, 'price': "7400", 'category_id': 2}
#     responce = client.post('/items',
#         json=test_data, headers={'Content-Type': 'application/json'})
    
#     assert responce.status_code == 201

#     conn = get_db()
#     cursor = conn.cursor()
#     cursor.execute("SELECT name, quantity, price, category_id FROM items")
#     result = cursor.fetchone()
#     conn.close()

#     assert result is not None
#     assert result['name'] == test_data['name']
#     assert result['quantity'] == test_data['quantity']
#     assert result['price'] == float(test_data['price'])
#     assert result['category_id'] == test_data['category_id']





