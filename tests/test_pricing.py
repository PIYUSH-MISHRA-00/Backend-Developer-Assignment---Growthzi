import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_price_default(client):
    response = client.get('/api/price')
    assert response.status_code == 200
    data = response.get_json()
    assert data['currency'] == 'USD'
    assert data['price'] == 100

def test_price_in(client):
    response = client.get('/api/price?country=IN')
    assert response.status_code == 200
    data = response.get_json()
    assert data['currency'] == 'INR'
    assert data['price'] == 8300

def test_price_unsupported_country(client):
    response = client.get('/api/price?country=XX')
    assert response.status_code == 400
    assert b"Unsupported country code" in response.data
