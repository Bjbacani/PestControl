from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class control_method(db.Model):
    __tablename__='control_method'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(45), nullable=False)
    
    def dict(self):
        return {
            "id": self.id,
            "type": self.type
            
        }
@app.route("/control_method", methods=["GET"])
def get_cm():
    cm = control_method.query.limit(100)
    return jsonify(
        {
            "success": True,
            "data": [cms.dict() for cms in cm]
        }
    ), 200
    
@app.route("/control_method/<int:id>", methods=['GET'])
def get_cms(id):
    cms = db.session.get(control_method, id)
    if not cms:
        return jsonify(
            {
                "success": False,
                "error": "control Method not found"
            }
        ), 400
    return jsonify(
        {
            "success": True,
            "data": cms.dict()
        }
    ), 200
    
@app.route("/control_method", methods=['POST'])
def add_cm():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "type"]
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400
            
    try:
        new_cm = control_method(
            id=data["id"],
            name=data["type"]
         )
        db.session.add(new_cm)
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
            "data": new_cm.dict()
        }
    ), 201


