import pytest
from unittest.mock import patch, Mock
from flask import json
from purchase import app, purchase, db

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

def create_mock_purchase():
    return type('MP', (), {
        "id": 1,
        "date": "2024-03-16",
        "product_id": 1,
        "customer_id": 1,
        "dict": lambda self: {
            "id": self.id,
            "date": self.date,
            "product_id": self.product_id,
            "customer_id": self.customer_id
        }
    })()

# Test GET all purchases
def test_get_purchases_success(client):
    mock_purchases = [create_mock_purchase()]
    with patch('purchase.purchase.query') as mock_query:
        mock_query.all.return_value = mock_purchases
        response = client.get("/purchase")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert len(data["data"]) == 1
        assert data["data"][0]["id"] == 1

def test_get_purchases_empty(client):
    with patch('purchase.purchase.query') as mock_query:
        mock_query.all.return_value = []
        response = client.get("/purchase")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert len(data["data"]) == 0

# Test GET single purchase
def test_get_single_purchase_success(client):
    mock_purchase = create_mock_purchase()
    with patch('purchase.db.session.get', return_value=mock_purchase):
        response = client.get("/purchase/1")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["data"]["id"] == 1

def test_get_single_purchase_not_found(client):
    with patch('purchase.db.session.get', return_value=None):
        response = client.get("/purchase/999")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["success"] is False
        assert "not found" in data["error"].lower()

# Test POST new purchase
def test_create_purchase_success(client):
    test_data = {
        "id": 1,
        "date": "2024-03-16",
        "product_id": 1,
        "customer_id": 1
    }
    
    mock_purchase = Mock()
    mock_purchase.dict.return_value = test_data
    
    with patch('purchase.purchase', return_value=mock_purchase):
        with patch('purchase.db.session.add'):
            with patch('purchase.db.session.commit'):
                response = client.post(
                    "/purchase",
                    data=json.dumps(test_data),
                    content_type='application/json'
                )
                assert response.status_code == 201
                data = json.loads(response.data)
                assert data["success"] is True
                assert data["data"]["id"] == test_data["id"]

def test_create_purchase_missing_fields(client):
    test_data = {
        "date": "2024-03-16",
        # missing required fields
    }
    response = client.post(
        "/purchase",
        data=json.dumps(test_data),
        content_type='application/json'
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "missing field" in data["error"].lower()

def test_create_purchase_invalid_content_type(client):
    response = client.post(
        "/purchase",
        data="not json data"
    )
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "content-type" in data["error"].lower()

# Test PUT (update) purchase
def test_update_purchase_success(client):
    mock_purchase = create_mock_purchase()
    update_data = {
        "date": "2024-03-17",
        "product_id": 2,
        "customer_id": 2
    }
    
    with patch('purchase.db.session.get', return_value=mock_purchase):
        with patch('purchase.db.session.commit'):
            response = client.put(
                "/purchase/1",
                data=json.dumps(update_data),
                content_type='application/json'
            )
            assert response.status_code == 200
            data = json.loads(response.data)
            assert data["success"] is True

def test_update_purchase_not_found(client):
    with patch('purchase.db.session.get', return_value=None):
        response = client.put(
            "/purchase/999",
            data=json.dumps({"date": "2024-03-17"}),
            content_type='application/json'
        )
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["success"] is False

# Test DELETE purchase
def test_delete_purchase_success(client):
    mock_purchase = create_mock_purchase()
    with patch('purchase.db.session.get', return_value=mock_purchase):
        with patch('purchase.db.session.delete') as mock_delete:
            with patch('purchase.db.session.commit'):
                response = client.delete("/purchase/1")
                mock_delete.assert_called_once_with(mock_purchase)
                assert response.status_code == 204

def test_delete_purchase_not_found(client):
    with patch('purchase.db.session.get', return_value=None):
        response = client.delete("/purchase/999")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["success"] is False

# Edge cases
def test_create_purchase_database_error(client):
    test_data = {
        "id": 1,
        "date": "2024-03-16",
        "product_id": 1,
        "customer_id": 1
    }
    
    with patch('purchase.db.session.add', side_effect=Exception("Database error")):
        response = client.post(
            "/purchase",
            data=json.dumps(test_data),
            content_type='application/json'
        )
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data["success"] is False
        assert "error" in data

def test_update_purchase_invalid_json(client):
    mock_purchase = create_mock_purchase()
    with patch('purchase.db.session.get', return_value=mock_purchase):
        response = client.put(
            "/purchase/1",
            data="invalid json",
            content_type='application/json'
        )
        assert response.status_code == 400