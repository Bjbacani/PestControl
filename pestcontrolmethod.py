from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class pest_control_methods(db.Model):
    __tablename__='pest_control_methods'
    id = db.Column(db.Integer, primary_key=True)
    Pest_id = db.Column(db.Integer, primary_key=True)
    Control_Method_id = db.Column(db.Integer, primary_key=True)
    
    def dict(self):
        return {
            "id": self.id,
            "Pest_id": self.Pest_id,
            "Control_Method_id": self.Control_Method_id
            
        }

@app.route("/pest_control_methods", methods=["GET"])
def get_pcm():
    pcm = pest_control_methods.query.limit(100)
    return jsonify(
        {
            "success": True,
            "data": [pcms.dict() for pcms in pcm]
        }
    ), 200

@app.route("/pest_control_methods/<int:id>", methods=['GET'])
def get_pcms(id):
    pcms = db.session.get(pest_control_methods, id)
    if not pcms:
        return jsonify(
            {
                "success": False,
                "error": " Not found"
            }
        ), 400
    return jsonify(
        {
            "success": True,
            "data": pcms.dict()
        }
    ), 200


@app.route("/pest_control_methods", methods=['POST'])
def add_pcm():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "Pest_id", "Control_Method_id"]
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400
            
    try:
        new_pcm = pest_control_methods(
            id=data["id"],
            Pest_id=data["Pest_id"],
            Control_Method_id=data["Control_Method_id"]
         )
        db.session.add(new_pcm)
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
            "data": new_pcm.dict()
        }
    ), 201

@app.route("/pest_control_methods/<int:id>", methods=["PUT"])
def update_pcm(id):
    prs = db.session.get(pest_control_methods, id)
    if not prs:
        return jsonify(
            {
                "success": False,
                "error": " Not found"
            }
        ), 404
    
    data = request.get_json()
    updatable_fields = ["id","Pest_id", "Control_Method_id"]
    
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
            "data": pest_control_methods.dict()
        }
    ), 200
