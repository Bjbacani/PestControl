from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class experiences(db.Model):
    __tablename__='experiences'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(45), nullable=False)
    product_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, primary_key=True)
    experience = db.Column(db.String(45), nullable=False)
    
    
    def dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "product_id": self.product_id,
            "customer_id": self.customer_id,
            "experience": self.experience
            
        }

@app.route("/experiences", methods=["GET"])
def get_prod():
    pr = experiences.query.limit(100)
    return jsonify(
        {
            "success": True,
            "data": [prs.dict() for prs in pr]
        }
    ), 200


@app.route("/experiences/<int:id>", methods=['GET'])
def get_prods(id):
    prs = db.session.get(experiences, id)
    if not prs:
        return jsonify(
            {
                "success": False,
                "error": "not found"
            }
        ), 400
    return jsonify(
        {
            "success": True,
            "data": prs.dict()
        }
    ), 200
