import pytest
from unittest.mock import patch
from flask import json
from experiences import app, experiences

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as client:
            yield client

def mtd(instance):
    return {
        "id": instance.id,
        "date": instance.date,
        "product_id": instance.product_id,
        "customer_id": instance.customer_id,
        "experience": instance.experience
    }

def test_get_experiences(client):
    mock_experiences = [
        type('ME', (object,), {
            "id": 1,
            "date": "10-10-2024",
            "product_id": 1,
            "customer_id": 1,
            "experience": "Great product",
            "dict": lambda self: mtd(self)
        })(),
        type('ME', (object,), {
            "id": 2,
            "date": "10-10-2024",
            "product_id": 2,
            "customer_id": 2,
            "experience": "Excellent service",
            "dict": lambda self: mtd(self)
        })()
    ]
    
    with patch('experiences.experiences.query', new_callable=lambda: type('Query', (), {'limit': lambda x: mock_experiences})):
        response = client.get("/experiences")
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert len(json_data["data"]) == 2
        assert json_data["data"][0]["experience"] == "Great product"

def test_single_experience(client):
    mock_experience = type('ME', (object,), {
        "id": 1,
        "date": "2-2-2000",
        "product_id": 1,
        "customer_id": 1,
        "experience": "Amazing product",
        "dict": lambda self: mtd(self)
    })()
    
    with patch('experiences.db.session.get', return_value=mock_experience):
        response = client.get("/experiences/1")
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert json_data["data"]["id"] == 1
        assert json_data["data"]["experience"] == "Amazing product"

def test_add_experience(client):
    new_experience_data = {
        "id": 1,
        "date": "15-03-2024",
        "product_id": 1,
        "customer_id": 1,
        "experience": "Very satisfied"
    }

    mock_experience = type('ME', (object,), {
        **new_experience_data,
        "dict": lambda self: new_experience_data
    })()

    with patch('experiences.experiences', return_value=mock_experience):
        with patch('experiences.db.session.add'):
            with patch('experiences.db.session.commit'):
                response = client.post("/experiences",
                                     data=json.dumps(new_experience_data),
                                     content_type='application/json')
                assert response.status_code == 201
                json_data = json.loads(response.data)
                assert json_data["success"] is True
                assert json_data["data"]["experience"] == "Very satisfied"

def test_update_experience(client):
    mock_experience = type('ME', (object,), {
        "id": 1,
        "date": "2-2-2000",
        "product_id": 1,
        "customer_id": 1,
        "experience": "Good",
        "dict": lambda self: mtd(self)
    })()

    update_data = {
        "id": 1,
        "date": "16-03-2024",
        "product_id": 1,
        "customer_id": 1,
        "experience": "Updated experience"
    }
    
    with patch('experiences.db.session.get', return_value=mock_experience):
        with patch.object(mock_experience, 'dict', return_value=update_data):
            response = client.put("/experiences/1",
                                data=json.dumps(update_data),
                                content_type='application/json')
            assert response.status_code == 200
            json_data = json.loads(response.data)
            assert json_data["success"] is True
            assert json_data["data"]["experience"] == "Updated experience"

def test_delete_experience(client):
    mock_experience = experiences(
        id=1,
        date="2-2-2023",
        product_id=1,
        customer_id=1,
        experience="Good product"
    )
    
    with patch('experiences.db.session.get', return_value=mock_experience):
        with patch('experiences.db.session.delete') as mock_delete:
            with patch('experiences.db.session.commit'):
                response = client.delete("/experiences/1")
                mock_delete.assert_called_once_with(mock_experience)
                assert response.status_code == 204