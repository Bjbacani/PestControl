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
                "error": "customer not found"
            }
        ), 400
    return jsonify(
        {
            "success": True,
            "data": crs.dict()
        }
    ), 200
    
    
@app.route("/customer", methods=['POST'])
def add_cust():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "name", "number", "location"]
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400
            
    try:
        new_c = customer(
            id=data["id"],
            name=data["name"],
            number=data["number"],
            location=data["location"]
         )
        db.session.add(new_c)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "success": False,
                "error": str(e)
            }
        ), 500
    
    return jsonify(
        {
            "success": True,
            "data": new_c.dict()
        }
    ), 201
    
@app.route("/customer/<int:id>", methods=["PUT"])
def update_c(id):
    crs = db.session.get(customer, id)
    if not crs:
        return jsonify(
            {
                "success": False,
                "error": "Customer not found"
            }
        ), 404
    
    data = request.get_json()
    updatable_fields = ["id","name", "number", "location"]
    
    for field in updatable_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": customer.dict()
        }
    ), 200

@app.route("/customer/<int:id>", methods=["DELETE"])
def delete_c(id):
    crs = db.session.get(customer, id)
    if not crs:
        return jsonify(
            {
                "success": True,
                "message": "customer successfully Deleted"
            }
        ), 204

if __name__ == 'main':
    app.run(debug=True)

