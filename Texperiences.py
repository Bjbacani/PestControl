import pytest
from unittest.mock import patch
from flask import json
from experiences import app, experiences


@pytest.fixture

def client ():
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

def tex(client):
    mkp = [
        type('experience', (object,), {
            "id":1,
            "date":"10-10-2021",
            "product_id":1,
            "customer_id":1,
            "experience":"I found the pest products to be very effective.",
            "dict": lambda self: mtd(self)
           
        })(),
         type('experience', (object,), {
            "id":2,
            "date":"12-10-2023",
            "product_id":2,
            "customer_id":2,
            "experience":"Using the pest products made a noticeable difference in controlling pests.",
            "dict": lambda self: mtd(self)
           
        })()
    ]
    with patch('experiences.experiences.query.all',return_value=tex):
        response = client.get("/experiences")
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert len(json_data["data"]) == 25
        assert json_data["data"][0]["date"] == "10-10-2037"
        