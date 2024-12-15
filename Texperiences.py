import pytest
from unittest.mock import patch
from flask import json
from experiences import app, test_experiences


@pytest.fixture
def test_client():
    app.config['TESTING'] = True
    with app.app_context():
        with app.test_client() as client:
            yield client
def test_mtd(instance):
    return {
         "id": instance.id,
         "date": instance.date,
         "product_id": instance.product_id,
         "customer_id": instance.customer_id,
         "experience": instance.experience
    }

def test_tex(client):
    mkp = [
        type('test_experiences', (object,), {
            "id":1,
            "date":"10-10-2021",
            "product_id":1,
            "customer_id":1,
            "experience":"I found the pest products to be very effective.",
            "dict": lambda self: test_mtd(self)
           
        })(),
         type('test_experiences', (object,), {
            "id":2,
            "date":"12-10-2023",
            "product_id":2,
            "customer_id":2,
            "experience":"Using the pest products made a noticeable difference in controlling pests.",
            "dict": lambda self: test_mtd(self)
           
        })()
    ]
    with patch('test_experiences.test_experiences.query.all',return_value=test_tex):
        response = client.get("/test_experiences")
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert len(json_data["data"]) == 25
        assert json_data["data"][0]["date"] == "10-10-2037"
        
def test_tsp(client):
        mkp = type('test_experiences', (object,),{
            "id":1,
            "date":"2-2-2000",
            "product_id":1,
            "customer_id":1,
            "experience":"Using the pest products made a noticeable difference in controlling pests.",
            "dict": lambda self: test_mtd(self)
            
        })()
        
        with patch('test_experiences.db.session.get', return_value=mkp):
            response = client.get("/test_experiences/1") 
            assert response.status_code == 200
            json_data = json.loads(response.data)
            assert json_data ["success"] is True
            assert json_data ["data"] ["id"] == 1
            assert json_data ["data"] ["experiences"] == "Using the pest products made a noticeable difference in controlling pests."
    
def test_tup(client):
        
    mkp = type('test_experiences', (object,),{
            "id":1,
            "date":"2-2-2026",
            "product_id":1,
            "customer_id":1,
            "experience":"Using the pest products made a noticeable difference in controlling pests.",
            "dict": lambda self: test_mtd(self)
            
    })()
    
    update_data = {
            "id":1,
            "date":"Updated 10-10-2035",
            "product_id":1,
            "customer_id":1,
            "experience":"Updated New expieriences is new"
           
            
    }
    
    with patch('test_experiences.db.session.get', return_value=mkp):
        response = client.put("/test_experiences/1",
                              data=json.dumps(update_data),
                              content_type='application/json')
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert json_data["data"]["date"] == "Updated 10-10-2025"
        assert json_data["data"]["experience"] == "Updated New expieriences is new"
        
def test_td(client):
    mkp = test_experiences(
        id =1,
        date="10-10-2021",
        product_id=1,
        customer_id=1,
        experience="I found the pest products to be very effective."
    )
        
    with patch('test_experiences.db.session.get',return_value=mkp):
        with patch('test_experiences.db.session.delete') as mkd:
            response = client.delete("/test_experiences/1")
            mkd.assert_called_once_with(mkp)
            assert response.status_code == 200
            json_data = json.loads(response.data)
            assert json_data["Success"] is True
            assert "DELETED" in json_data["message"]
                              

