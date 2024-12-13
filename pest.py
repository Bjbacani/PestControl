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

@app.route("/pest", methods=['POST'])
def add_pest():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "name"]
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400
            
    try:
        new_pest = pest(
            id=data["id"],
            name=data["name"]
         )
        db.session.add(new_pest)
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
            "data": new_pest.dict()
        }
    ), 201

@app.route("/pest/<int:id>", methods=["PUT"])
def update_pest(id):
    Pests = db.session.get(pest, id)
    if not Pests:
        return jsonify(
            {
                "success": False,
                "error": "Pest not found"
            }
        ), 404
    
    data = request.get_json()
    updatable_fields = ["id","name"]
    
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
            "data": pest.dict()
        }
    ), 200

