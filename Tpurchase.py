import pytest
from unittest.mock import patch
from flask import json
from purchase import app, purchase


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
         "customer_id": instance.customer_id
    }

def tg_pest(client):
    mkp = [
        type('MP', (object,), {
            "id":1,
            "date":"10-10-2024",
            "product_id":1,
            "customer_id":1,
            "dict": lambda self: mtd(self)
           
        })(),
         type('MP', (object,), {
            "id":2,
            "date":"10-10-2024",
            "product_id":2,
            "customer_id":2,
            "dict": lambda self: mtd(self)
           
        })()
    ]
    with patch('purchase.purchase.query.all',return_value=tg_pest):
        response = client.get("/purchase")
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert len(json_data["data"]) == 25
        assert json_data["data"][0]["date"] == "10-10-2029"
        
def tsp(client):
        mkp = type('MP', (object,),{
            "id":1,
            "date":"2-2-2000",
            "product_id":1,
            "customer_id":1,
            "dict": lambda self: mtd(self)
            
        })()
        
        with patch('purchase.db.session.get', return_value=mkp):
            response = client.get("/purchase/1") 
            assert response.status_code == 200
            json_data = json.loads(response.data)
            assert json_data ["success"] is True
            assert json_data ["data"] ["id"] == 1
            assert json_data ["data"] ["date"] == "2-2-2000"
    
def tup(client):
        
    mkp = type('MP', (object,),{
            "id":1,
            "date":"2-2-2000",
            "product_id":1,
            "customer_id":1,
            "dict": lambda self: mtd(self)
            
    })()
    
    update_data = {
            "id":1,
            "date":"Updated 10-10-2025",
            "product_id":1,
            "customer_id":1
            
    }
    
    with patch('purchase.db.session.get', return_value=mkp):
        response = client.put("/purchase/1",
                              data=json.dumps(update_data),
                              content_type='application/json')
        assert response.status_code == 200
        json_data = json.loads(response.data)
        assert json_data["success"] is True
        assert json_data["data"]["date"] == "Updated 10-10-2025"
        
def td(client):
    mkp = purchase(
        id =1,
        date="2-2-2023",
        product_id=1,
        customer_id=1
    )
        
    with patch('purchase.db.session.get',return_value=mkp):
        with patch('purchase.db.session.delete') as mkd:
            response = client.delete("/purchase/1")
            mkd.assert_called_once_with(mkp)
            assert response.status_code == 200
            json_data = json.loads(response.data)
            assert json_data["Success"] is True
            assert "DELETED" in json_data["message"]
                              
    
        
        