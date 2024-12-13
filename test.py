import pytest
from unittest.mock import patch
from datetime import datetime
from app import app, pest

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def tg_pest(client):
    mkp = [
        pest(
            id=1,
            name="cockroach",
           
        ),
        pest(
            id=2,
            name="insect",
          
        ),
    ]
    
    with app.app_context():
        with patch("app.pest.query.all") as mock_all:
            mock_all.return_value = mkp
            response = client.get("/pest")
            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data["success"] is True
            assert len(json_data["data"]) == 100

def tg_pests(client):
    mkps = pest(
         id=1,
         name="cockroach",
    )

    with app.app_context():
        with patch("app.pest.query.get") as mock_get:
            mock_get.return_value = mkps
            response = client.get("/pest/1")
            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data["success"] is True
            assert json_data["data"]["id"] == 1

def tup(client):
    ep = pest(
         id=1,
         name="cockroach",
    )

    with app.app_context():
        with patch("app.pest.query.get") as mock_get, patch("app.db.session.commit", autospec=True):
            mock_get.return_value = ep
            updated_data = {
                "name": "Updated cockroachjr",
            }
            response = client.put("/pest/1", json=updated_data)
            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data["success"] is True
            assert json_data["data"]["name"] == "Updated cockroachjr"



