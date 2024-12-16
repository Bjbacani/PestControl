from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class purchase(db.Model):
    __tablename__='purchase'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(45), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    
    def dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "product_id": self.product_id,
            "customer_id": self.customer_id
        }

@app.route("/purchase", methods=["GET"])
def get_purchases():
    purchases = purchase.query.all()
    return jsonify(
        {
            "success": True,
            "data": [p.dict() for p in purchases]
        }
    ), 200

@app.route("/purchase/<int:id>", methods=['GET'])
def get_purchase(id):
    purch = db.session.get(purchase, id)
    if not purch:
        return jsonify(
            {
                "success": False,
                "error": "Purchase not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": purch.dict()
        }
    ), 200

@app.route("/purchase", methods=['POST'])
def add_purchase():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "date", "product_id", "customer_id"]
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400
            
    try:
        new_purchase = purchase(
            id=data["id"],
            date=data["date"],
            product_id=data["product_id"],
            customer_id=data["customer_id"]
        )
        db.session.add(new_purchase)
        db.session.commit()
        
        return jsonify(
            {
                "success": True,
                "data": new_purchase.dict()
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

@app.route("/purchase/<int:id>", methods=["PUT"])
def update_purchase(id):
    purch = db.session.get(purchase, id)
    if not purch:
        return jsonify(
            {
                "success": False,
                "error": "Purchase not found"
            }
        ), 404
    
    data = request.get_json()
    updatable_fields = ["date", "product_id", "customer_id"]
    
    for field in updatable_fields:
        if field in data:
            setattr(purch, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": purch.dict()
        }
    ), 200

@app.route("/purchase/<int:id>", methods=["DELETE"])
def delete_purchase(id):
    purch = db.session.get(purchase, id)
    if not purch:
        return jsonify(
            {
                "success": False,
                "error": "Purchase not found"
            }
        ), 404
        
    db.session.delete(purch)
    db.session.commit()
    
    return jsonify(
        {
            "success": True,
            "message": "Successfully deleted"
        }
    ), 204

if __name__ == '__main__':
    try:
        with app.app_context():
            db.create_all()
            print("Database tables created successfully!")
    except Exception as e:
        print(f"Error: {e}")
    
    app.run(debug=True, port=5002)