import pytest
from unittest.mock import patch, MagicMock
from flask import json
from pestcontrol import app, customer, products, purchase, experiences, db

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

# Mock data creators
def create_mock_customer():
    return {
        "id": 1,
        "name": "John Doe",
        "number": "1234567890",
        "location": "New York"
    }

def create_mock_product():
    return {
        "id": 1,
        "name": "Test Product",
        "detail": "Product Details"
    }

def create_mock_purchase():
    return {
        "id": 1,
        "date": "2024-03-16",
        "product_id": 1,
        "customer_id": 1
    }

def create_mock_experience():
    return {
        "id": 1,
        "date": "2024-03-16",
        "product_id": 1,
        "customer_id": 1,
        "experience": "Great service"
    }

# Customer Tests
class TestCustomer:
    def test_get_customers_success(self, client):
        mock_cust = customer(**create_mock_customer())
        with patch('pestcontrol.customer.query') as mock_query:
            mock_query.all.return_value = [mock_cust]
            response = client.get("/customer")
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True
            assert len(data["data"]) == 1

    def test_get_customer_success(self, client):
        mock_cust = customer(**create_mock_customer())
        with patch('pestcontrol.db.session.get') as mock_get:
            mock_get.return_value = mock_cust
            response = client.get("/customer/1")
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True

    def test_create_customer_success(self, client):
        mock_data = create_mock_customer()
        response = client.post("/customer",
                             data=json.dumps(mock_data),
                             content_type='application/json')
        assert response.status_code == 201

# Product Tests
class TestProduct:
    def test_get_products_success(self, client):
        mock_prod = products(**create_mock_product())
        with patch('pestcontrol.products.query') as mock_query:
            mock_query.limit.return_value = [mock_prod]
            response = client.get("/products")
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True

    def test_get_product_success(self, client):
        mock_prod = products(**create_mock_product())
        with patch('pestcontrol.db.session.get') as mock_get:
            mock_get.return_value = mock_prod
            response = client.get("/products/1")
            assert response.status_code == 200

    def test_create_product_success(self, client):
        mock_data = create_mock_product()
        response = client.post("/products",
                             data=json.dumps(mock_data),
                             content_type='application/json')
        assert response.status_code == 201

# Purchase Tests
class TestPurchase:
    def test_get_purchases_success(self, client):
        mock_purch = purchase(**create_mock_purchase())
        with patch('pestcontrol.purchase.query') as mock_query:
            mock_query.all.return_value = [mock_purch]
            response = client.get("/purchase")
            assert response.status_code == 200

    def test_get_purchase_success(self, client):
        mock_purch = purchase(**create_mock_purchase())
        with patch('pestcontrol.db.session.get') as mock_get:
            mock_get.return_value = mock_purch
            response = client.get("/purchase/1")
            assert response.status_code == 200

    def test_create_purchase_success(self, client):
        mock_data = create_mock_purchase()
        response = client.post("/purchase",
                             data=json.dumps(mock_data),
                             content_type='application/json')
        assert response.status_code == 201

# Experience Tests
class TestExperience:
    def test_get_experiences_success(self, client):
        mock_exp = experiences(**create_mock_experience())
        with patch('pestcontrol.experiences.query') as mock_query:
            mock_query.limit.return_value = [mock_exp]
            response = client.get("/experiences")
            assert response.status_code == 200

    def test_get_experience_success(self, client):
        mock_exp = experiences(**create_mock_experience())
        with patch('pestcontrol.db.session.get') as mock_get:
            mock_get.return_value = mock_exp
            response = client.get("/experiences/1")
            assert response.status_code == 200

    def test_create_experience_success(self, client):
        mock_data = create_mock_experience()
        response = client.post("/experiences",
                             data=json.dumps(mock_data),
                             content_type='application/json')
        assert response.status_code == 201

# Edge Cases and Error Tests
def test_invalid_content_type(client):
    response = client.post("/customer",
                          data="not json")
    assert response.status_code == 400

def test_missing_required_fields(client):
    invalid_data = {"name": "Test"}
    response = client.post("/customer",
                          data=json.dumps(invalid_data),
                          content_type='application/json')
    assert response.status_code == 400

def test_database_error(client):
    mock_data = create_mock_customer()
    with patch('pestcontrol.db.session.commit') as mock_commit:
        mock_commit.side_effect = Exception("Database error")
        response = client.post("/customer",
                             data=json.dumps(mock_data),
                             content_type='application/json')
        assert response.status_code == 500

def test_not_found_errors(client):
    with patch('pestcontrol.db.session.get', return_value=None):
        endpoints = ["/customer/999", "/products/999", 
                    "/purchase/999", "/experiences/999"]
        for endpoint in endpoints:
            response = client.get(endpoint)
            assert response.status_code in [404, 400]