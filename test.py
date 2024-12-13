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


