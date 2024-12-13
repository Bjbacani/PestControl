from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class pest(db.Model):
    __tablename__='pest'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name
            
        }
        
@app.route("/pest", methods=["GET"])
def get_pests():
    Pest = pest.query.limit(100)
    return jsonify(
        {
            "success": True,
            "data": [Pests.dict() for Pests in Pest]
        }
    ), 200

@app.route("/pest/<int:id>", methods=['GET'])
def get_pest(id):
    Pests = db.session.get(pest, id)
    if not Pests:
        return jsonify(
            {
                "success": False,
                "error": "Pest not found"
            }
        ), 400
    return jsonify(
        {
            "success": True,
            "data": Pests.dict()
        }
    ), 200

