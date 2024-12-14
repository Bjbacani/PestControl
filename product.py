from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class products(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    detail = db.Column(db.String(45), nullable=False)
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "detail": self.detail
            
        }

@app.route("/products", methods=["GET"])
def get_prod():
    pr = products.query.limit(100)
    return jsonify(
        {
            "success": True,
            "data": [prs.dict() for prs in pr]
        }
    ), 200

@app.route("/products/<int:id>", methods=['GET'])
def get_prods(id):
    prs = db.session.get(products, id)
    if not prs:
        return jsonify(
            {
                "success": False,
                "error": "Product not found"
            }
        ), 400
    return jsonify(
        {
            "success": True,
            "data": prs.dict()
        }
    ), 200

@app.route("/products", methods=['POST'])
def add_prod():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "name", "detail"]
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400
            
    try:
        new_pr = products(
            id=data["id"],
            name=data["name"],
            detail=data["detail"]
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

@app.route("/products/<int:id>", methods=["PUT"])
def update_pr(id):
    prs = db.session.get(products, id)
    if not prs:
        return jsonify(
            {
                "success": False,
                "error": "Product not found"
            }
        ), 404
    
    data = request.get_json()
    updatable_fields = ["id","name", "detail"]
    
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
            "data": products.dict()
        }
    ), 200
    
@app.route("/products/<int:id>", methods=["DELETE"])
def delete_pr(id):
    prs = db.session.get(products, id)
    if not prs:
        return jsonify(
            {
                "success": True,
                "message": "Product successfully Deleted"
            }
        ), 204

if __name__ == 'main':
    app.run(debug=True)