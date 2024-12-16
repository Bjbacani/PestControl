from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class customer(db.Model):
    __tablename__ = 'customer'
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

# Add these route handlers
@app.route("/customer", methods=["GET"])
def get_customers():
    customers = customer.query.all()
    return jsonify(
        {
            "success": True,
            "data": [c.dict() for c in customers]
        }
    ), 200

@app.route("/customer/<int:id>", methods=['GET'])
def get_customer(id):
    cust = db.session.get(customer, id)
    if not cust:
        return jsonify(
            {
                "success": False,
                "error": "Customer not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": cust.dict()
        }
    ), 200


@app.route("/customer", methods=['POST'])
def add_customer():
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
        new_customer = customer(
            id=data["id"],
            name=data["name"],
            number=data["number"],
            location=data["location"]
        )
        db.session.add(new_customer)
        db.session.commit()
        
        return jsonify(
            {
                "success": True,
                "data": new_customer.dict()
            }
        ), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(
            {
                "success": False,
                "error": str(e)
            }
        ), 500



@app.route("/customer/<int:id>", methods=["PUT"])
def update_customer(id):
    cust = db.session.get(customer, id)
    if not cust:
        return jsonify(
            {
                "success": False,
                "error": "Customer not found"
            }
        ), 404
    
    data = request.get_json()
    updatable_fields = ["name", "number", "location"]
    
    for field in updatable_fields:
        if field in data:
            setattr(cust, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": cust.dict()
        }
    ), 200
