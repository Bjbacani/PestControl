import pytest
from unittest.mock import patch, MagicMock
from flask import json
from experiences import app, experiences, db

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

def create_mock_experience():
    return {
        "id": 1,
        "date": "2024-03-16",
        "product_id": 1,
        "customer_id": 1,
        "experience": "Test Experience"
    }

# Test GET all experiences
def test_get_experiences_success(client):
    # Mock data
    mock_exp = experiences(**create_mock_experience())
    with patch('experiences.experiences.query') as mock_query:
        mock_query.limit.return_value = [mock_exp]
        
        response = client.get("/experiences")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert len(data["data"]) == 1
        assert data["data"][0]["experience"] == "Test Experience"

# Test GET single experience
def test_get_experience_success(client):
    mock_exp = experiences(**create_mock_experience())
    with patch('experiences.db.session.get') as mock_get:
        mock_get.return_value = mock_exp
        
        response = client.get("/experiences/1")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["data"]["id"] == 1

def test_get_experience_not_found(client):
    with patch('experiences.db.session.get') as mock_get:
        mock_get.return_value = None
        
        response = client.get("/experiences/999")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["success"] is False
        assert "not found" in data["error"].lower()

# Test POST experience
def test_create_experience_success(client):
    mock_data = create_mock_experience()
    
    with patch('experiences.db.session.add'), \
         patch('experiences.db.session.commit'):
        response = client.post("/experiences",
                             data=json.dumps(mock_data),
                             content_type='application/json')
        assert response.status_code == 201
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["data"]["experience"] == mock_data["experience"]

def test_create_experience_missing_field(client):
    invalid_data = create_mock_experience()
    del invalid_data["experience"]
    
    response = client.post("/experiences",
                          data=json.dumps(invalid_data),
                          content_type='application/json')
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "missing field" in data["error"].lower()

def test_create_experience_invalid_content_type(client):
    response = client.post("/experiences",
                          data="not json")
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data["success"] is False
    assert "content-type" in data["error"].lower()

# Test PUT experience
def test_update_experience_success(client):
    mock_exp = experiences(**create_mock_experience())
    update_data = {"experience": "Updated Experience"}
    
    with patch('experiences.db.session.get') as mock_get, \
         patch('experiences.db.session.commit'):
        mock_get.return_value = mock_exp
        
        response = client.put("/experiences/1",
                            data=json.dumps(update_data),
                            content_type='application/json')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["success"] is True
        assert data["data"]["experience"] == "Updated Experience"

def test_update_experience_not_found(client):
    with patch('experiences.db.session.get') as mock_get:
        mock_get.return_value = None
        
        response = client.put("/experiences/999",
                            data=json.dumps({"experience": "Test"}),
                            content_type='application/json')
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["success"] is False

# Test DELETE experience
def test_delete_experience_success(client):
    mock_exp = experiences(**create_mock_experience())
    with patch('experiences.db.session.get') as mock_get, \
         patch('experiences.db.session.delete') as mock_delete, \
         patch('experiences.db.session.commit'):
        mock_get.return_value = mock_exp
        
        response = client.delete("/experiences/1")
        assert response.status_code == 204
        mock_delete.assert_called_once_with(mock_exp)

def test_delete_experience_not_found(client):
    with patch('experiences.db.session.get') as mock_get:
        mock_get.return_value = None
        
        response = client.delete("/experiences/999")
        assert response.status_code == 404
        data = json.loads(response.data)
        assert data["success"] is False

# Test database errors
def test_create_experience_db_error(client):
    mock_data = create_mock_experience()
    
    with patch('experiences.db.session.add') as mock_add, \
         patch('experiences.db.session.commit') as mock_commit:
        mock_commit.side_effect = Exception("Database error")
        
        response = client.post("/experiences",
                             data=json.dumps(mock_data),
                             content_type='application/json')
        assert response.status_code == 500
        data = json.loads(response.data)
        assert data["success"] is False
        assert "error" in data