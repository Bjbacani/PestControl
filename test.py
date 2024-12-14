import pytest
from unittest.mock import patch
from purchase import app, purchase

# Fixture for the test client
@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

# Test case for getting all purchases
def test_get_purchases(client):
    mock_purchases = [
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
        with patch("purchase.query.all") as mock_all:
            mock_all.return_value = mock_purchases
            response = client.get("/purchase")

            # Assert response status code
            assert response.status_code == 200

            # Parse JSON response
            json_data = response.get_json()

            # Assert success and data length
            assert json_data["success"] is True
            assert len(json_data["data"]) == len(mock_purchases)

# Test case for getting a specific purchase by ID
def test_get_purchase_by_id(client):
    mock_purchase = purchase(
        id=1,
        date="5/19/2014",
        product_id=1,
        customer_id=1
    )

    with app.app_context():
        with patch("purchase.query.get") as mock_get:
            mock_get.return_value = mock_purchase
            response = client.get("/purchase/1")

            # Assert response status code
            assert response.status_code == 200

            # Parse JSON response
            json_data = response.get_json()

            # Assert success and returned data
            assert json_data["success"] is True
            assert json_data["data"]["id"] == 1

# Test case for updating a purchase
def test_update_purchase(client):
    mock_purchase = purchase(
        id=1,
        date="5/19/2014",
        product_id=1,
        customer_id=1
    )

    with app.app_context():
        with patch("purchase.query.get") as mock_get, patch("app.db.session.commit", autospec=True):
            mock_get.return_value = mock_purchase
            updated_data = {
                "date": "2/12/2024",
            }
            response = client.put("/purchase/1", json=updated_data)

            # Assert response status code
            assert response.status_code == 200

            # Parse JSON response
            json_data = response.get_json()

            # Assert success and updated data
            assert json_data["success"] is True
            assert json_data["data"]["date"] == "2/12/2024"

# Test case for deleting a purchase
def test_delete_purchase(client):
    mock_purchase = purchase(
        id=1,
        date="5/19/2014",
        product_id=1,
        customer_id=1
    )

    with app.app_context():
        with patch("purchase.query.get") as mock_get, patch("app.db.session.delete"), patch("app.db.session.commit"):
            mock_get.return_value = mock_purchase
            response = client.delete("/purchase/1")

            # Assert response status code
            assert response.status_code == 204

            # Assert empty response body
            assert response.data == b''
