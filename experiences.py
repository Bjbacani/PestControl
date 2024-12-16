from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class experiences(db.Model):
    __tablename__ = 'experiences'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(45), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.String(255), nullable=False)
    
    def dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "product_id": self.product_id,
            "customer_id": self.customer_id,
            "experience": self.experience
        }

@app.route("/experiences", methods=["GET"])
def get_experiences():
    exp = experiences.query.limit(100)
    return jsonify(
        {
            "success": True,
            "data": [e.dict() for e in exp]
        }
    ), 200

@app.route("/experiences/<int:id>", methods=['GET'])
def get_experience(id):
    exp = db.session.get(experiences, id)
    if not exp:
        return jsonify(
            {
                "success": False,
                "error": "Experience not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": exp.dict()
        }
    ), 200

@app.route("/experiences", methods=['POST'])
def add_experience():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "date", "product_id", "customer_id", "experience"]
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400
            
    try:
        new_experience = experiences(
            id=data["id"],
            date=data["date"],
            product_id=data["product_id"],
            customer_id=data["customer_id"],
            experience=data["experience"]
        )
        db.session.add(new_experience)
        db.session.commit()
        
        return jsonify(
            {
                "success": True,
                "data": new_experience.dict()
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

@app.route("/experiences/<int:id>", methods=["PUT"])
def update_experience(id):
    exp = db.session.get(experiences, id)
    if not exp:
        return jsonify(
            {
                "success": False,
                "error": "Experience not found"
            }
        ), 404
    
    data = request.get_json()
    updatable_fields = ["date", "product_id", "customer_id", "experience"]
    
    for field in updatable_fields:
        if field in data:
            setattr(exp, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": exp.dict()
        }
    ), 200

@app.route("/experiences/<int:id>", methods=["DELETE"])
def delete_experience(id):
    exp = db.session.get(experiences, id)
    if not exp:
        return jsonify(
            {
                "success": False,
                "error": "Experience not found"
            }
        ), 404
        
    db.session.delete(exp)
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
    
    app.run(debug=True, port=5003)