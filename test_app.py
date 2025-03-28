import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_category(client):
    response = client.post('/category', json={'name': 'Electronics'})
    assert response.status_code == 201
    assert b'Electronics' in response.data

def test_add_item(client):
    client.post('/category', json={'name': 'Electronics'})
    response = client.post('/item', json={
        'name': 'Laptop',
        'quantity': 10,
        'price': 999.99,
        'category_id': 1
    })
    assert response.status_code == 201
    assert b'Laptop' in response.data