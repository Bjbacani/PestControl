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
