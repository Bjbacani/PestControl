from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class customer(db.Model):
    __tablename__='customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    number = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(45), nullable=False)
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "number": self.number,
            "location": self.location
            
            
        }
@app.route("/customer", methods=["GET"])
def get_c():
    cr = customer.query.limit(100)
    return jsonify(
        {
            "success": True,
            "data": [crs.dict() for crs in cr]
        }
    ), 200

@app.route("/customer/<int:id>", methods=['GET'])
def get_cs(id):
    crs = db.session.get(customer, id)
    if not crs:
        return jsonify(
            {
                "success": False,
                "error": "Product not found"
            }
        ), 400
    return jsonify(
        {
            "success": True,
            "data": crs.dict()
        }
    ), 200
