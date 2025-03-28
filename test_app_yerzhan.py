import pytest
from app import app, categories, items, customers



def test_add_to_basket(client):
    # Подготовка данных
    customers.clear()
    items.clear()
    client.post('/customers', json={
        'username': 'testuser',
        'password': 'password123',
        'email': 'test@example.com'
    })
    client.post('/items', json={
        'name': 'Keyboard',
        'quantity': 15,
        'price': 49.99,
        'category_id': 1,
        'image': 'keyboard.jpg'
    })
    
    response = client.post('/customers/1/basket', json={
        'item_id': 1,
        'quantity': 2
    })
    assert response.status_code == 200
    assert len(customers[0]['basket']) == 1

def test_generate_report(client):
    # Подготовка данных
    customers.clear()
    items.clear()
    client.post('/customers', json={
        'username': 'testuser',
        'password': 'password123',
        'email': 'test@example.com'
    })
    client.post('/items', json={
        'name': 'Mouse',
        'quantity': 20,
        'price': 29.99,
        'category_id': 1,
        'image': 'mouse.jpg'
    })
    client.post('/customers/1/basket', json={
        'item_id': 1,
        'quantity': 1
    })
    
    response = client.get('/report')
    assert response.status_code == 200
    assert b'Mouse' in response.data
    assert b'testuser' in response.data