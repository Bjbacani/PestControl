import pytest
from unittest.mock import patch
from purchase import app, purchase


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def tg_pest(client):
    mkp = [
        purchase(
            id=1,
            date="5/19/2014",
            product_id=1,
            customer_id=1
        ),
        purchase(
            id=2,
            date="2/13/2021",
            product_id=2,
            customer_id=2
          
        ),
    ]
    
    with app.app_context():
        with patch("test.purchase.query.all") as mock_all:
            mock_all.return_value = mkp
            response = client.get("/purchase")
            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data["success"] is True
            assert len(json_data["data"]) == 100

def tg_pests(client):
    mkps = purchase(
         id=1,
         date="5/19/2014",
         product_id=1,
         customer_id=1
    )

    with app.app_context():
        with patch("test.purchase.query.get") as mock_get:
            mock_get.return_value = mkps
            response = client.get("/purchase/1")
            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data["success"] is True
            assert json_data["data"]["id"] == 1

def tup(client):
    ep = purchase(
         id=1,
         date="5/19/2014",
         product_id=1,
         customer_id=1
    )

    with app.app_context():
        with patch("app.purchase.query.get") as mock_get, patch("app.db.session.commit", autospec=True):
            mock_get.return_value = ep
            updated_data = {
                "date": "2/12/2024",
            }
            response = client.put("/purchase/1", json=updated_data)
            assert response.status_code == 200
            json_data = response.get_json()
            assert json_data["success"] is True
            assert json_data["data"]["date"] == "Updated 2/12/2024"
            
def tdp(client):
    with app.app_context():
        with patch("app.purchase.query.get") as mock_get, patch("app.db.session.delete"), patch("app.db.session.commit"):
            mkps = purchase(
                id=1,
                date="5/19/2014",
                product_id=1,
                customer_id=1
            )
            mock_get.return_value = mkps
            response = client.delete("/purchase/1")
            assert response.status_code == 204
            assert response.data == b''


