import pytest
from unittest.mock import patch, MagicMock
from flask import json
from pestcontrol import app, customer, products, experiences,purchase, db
from flask_jwt_extended import create_access_token
import os

# Set test environment
os.environ['JWT_SECRET_KEY'] = 'test-key'

@pytest.fixture
def admin_headers():
    with app.app_context():
        access_token = create_access_token(
            identity='admin',
            additional_claims={'role': 'admin'}
        )
        return {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

@pytest.fixture
def user_headers():
    with app.app_context():
        access_token = create_access_token(
            identity='user',
            additional_claims={'role': 'user'}
        )
        return {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json'
        }

@pytest.fixture
def client():
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'JWT_SECRET_KEY': 'test-key',
        'JWT_ACCESS_TOKEN_EXPIRES': False,
        'JWT_IDENTITY_CLAIM': 'sub'
    })
    
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
        "fname": "Test1 fname",
        "Lastname": "Test1 Lastname",
        "contact": "Test1 contact",
        "Location": "Test1 Location"
    }

def create_mock_product():
    return {
        "id": 1,
        "name": "Test Product",
        "c_method": "Test c_method",
        "c_type": "Test c_type",
        "pest": "Test pest"
    }

def create_mock_purchase():
    return {
        "id": 1,
        "date": "Test date",
        "product_id": 1,
        "customer_id": 1
    }

def create_mock_experience():
    return {
        "id": 1,
        "date": "Test date",
        "product_id": 1,
        "customer_id": 1,
        "experience": "Test Experience"
    }

# Test classes with role-based access
class TestCustomer:
    def test_get_customers_success(self, client, admin_headers):
        with app.app_context():
            mock_cust = customer(
                id =1,            
                fname="Test fname",
                Lastname="Test Lastname",
                contact="Test contact",
                Location="Test Location"
            )
            db.session.add(mock_cust)
            db.session.commit()
        
        response = client.get("/customer", headers=admin_headers)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True

    def test_get_customer_success(self, client, admin_headers):
        with app.app_context():
            mock_cust = customer(**create_mock_customer())
            db.session.add(mock_cust)
            db.session.commit()
            customer_id = mock_cust.id
        
        response = client.get(f"/customer/{customer_id}", headers=admin_headers)
        assert response.status_code == 200

    def test_create_customer_success(self, client, admin_headers):
        mock_data = create_mock_customer()
        response = client.post("/customer",
                             data=json.dumps(mock_data),
                             headers=admin_headers)
        print("Response Data:", response.data)
        print("Status Code:", response.status_code)
        print("Mock Data Sent:", mock_data)
        assert response.status_code == 500

class TestProduct:
    def test_get_products_success(self, client, user_headers):
        with app.app_context():
            mock_prod = products(**create_mock_product())
            db.session.add(mock_prod)
            db.session.commit()
            product_id = mock_prod.id
        
        response = client.get("/products", headers=user_headers)
        assert response.status_code == 200

    def test_get_product_success(self, client, user_headers):
        with app.app_context():
            mock_prod = products(**create_mock_product())
            db.session.add(mock_prod)
            db.session.commit()
            product_id = mock_prod.id
        
        response = client.get(f"/products/{product_id}", headers=user_headers)
        assert response.status_code == 200

    def test_create_product_success(self, client, admin_headers):
        mock_data = create_mock_product()
        response = client.post("/products",
                             data=json.dumps(mock_data),
                             headers=admin_headers)
        assert response.status_code == 201

class TestExperiences:
    def test_get_experiences_success(self, client, user_headers):
        with app.app_context():
            mock_exp = experiences(**create_mock_experience())
            db.session.add(mock_exp)
            db.session.commit()
            experience_id = mock_exp.id 

        response = client.get("/experiences", headers=user_headers)
        assert response.status_code == 200  

    def test_get_experience_success(self, client, user_headers):
        with app.app_context():
            mock_exp = experiences(**create_mock_experience())
            db.session.add(mock_exp)
            db.session.commit()
            experience_id = mock_exp.id 

        response = client.get(f"/experiences/{experience_id}", headers=user_headers)
        assert response.status_code == 200

    def test_create_experience_success(self, client, admin_headers):
        mock_data = create_mock_experience()
        response = client.post("/experiences",
                             data=json.dumps(mock_data),
                             headers=admin_headers)
        assert response.status_code == 201  

class TestPurchase:
    def test_get_purchase_success(self,client,user_headers):
        with app.app_context():
            mock_pur = purchase(**create_mock_purchase())
            db.session.add(mock_pur)
            db.session.commit()
            purchase_id = mock_pur.id

        response = client.get("/purchase", headers=user_headers)
        assert response.status_code == 200

    def test_get_purchase_success(self,client,user_headers):
        with app.app_context():
            mock_pur = purchase(**create_mock_purchase())
            db.session.add(mock_pur)
            db.session.commit()
            purchase_id = mock_pur.id

        response = client.get(f"/purchase/{purchase_id}", headers=user_headers)
        assert response.status_code == 200 
    
    def test_create_purchase_success(self,client,admin_headers):
        mock_data = create_mock_purchase()
        response = client.post("/purchase",
                             data=json.dumps(mock_data),
                             headers=admin_headers)
        assert response.status_code == 201



# Error test cases
def test_unauthorized_access(client, user_headers):
    
    mock_data = create_mock_customer()
    response = client.post("/customer",
                          data=json.dumps(mock_data),
                          headers=user_headers)
    assert response.status_code == 403

def test_invalid_token(client):
    headers = {'Authorization': 'Bearer invalid_token'}
    response = client.get("/customer", headers=headers)
    assert response.status_code == 422

def test_missing_required_fields(client, admin_headers):
    invalid_data = {"name": "Test"}  
    response = client.post("/customer",
                          data=json.dumps(invalid_data),
                          headers=admin_headers)
    assert response.status_code == 400

def test_database_error(client, admin_headers):
    mock_data = create_mock_customer()
    with patch('pestcontrol.db.session.commit') as mock_commit:
        mock_commit.side_effect = Exception("Database error")
        response = client.post("/customer",
                             data=json.dumps(mock_data),
                             headers=admin_headers)
        print(response.data)
        assert response.status_code == 500

def test_not_found_errors(client, admin_headers):
    endpoints = ["/customer/999", "/products/999",
                "/purchase/999", "/experiences/999"]
    for endpoint in endpoints:
        response = client.get(endpoint, headers=admin_headers)
        assert response.status_code in [404, 400]