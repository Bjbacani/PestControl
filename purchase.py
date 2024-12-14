from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class purchase(db.Model):
    __tablename__='purchase'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(45), nullable=False)
    product_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, primary_key=True)
    
    
    def dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "product_id": self.product_id,
            "customer_id": self.customer_id,
            
        }

@app.route("/purchase", methods=["GET"])
def get_prod():
    pr = purchase.query.limit(100)
    return jsonify(
        {
            "success": True,
            "data": [prs.dict() for prs in pr]
        }
    ), 200


@app.route("/purchase/<int:id>", methods=['GET'])
def get_prods(id):
    prs = db.session.get(purchase, id)
    if not prs:
        return jsonify(
            {
                "success": False,
                "error": "purchase not found"
            }
        ), 400
    return jsonify(
        {
            "success": True,
            "data": prs.dict()
        }
    ), 200

@app.route("/purchase", methods=['POST'])
def add_prod():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "date","product_id", "customer_id"]
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400
            
    try:
        new_pr = purchase(
            id=data["id"],
            name=data["name"],
            product_id=data["product_id"],
            customer_id=data["customer_id"]
         )
        db.session.add(new_pr)
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
            "data": new_pr.dict()
        }
    ), 201
