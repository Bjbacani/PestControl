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
