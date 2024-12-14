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
