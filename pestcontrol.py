from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:password@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False)
    number = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(45), nullable=False)
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "number": self.number,
            "location": self.location
        }

# Add these route handlers
@app.route("/customer", methods=["GET"])
def get_customers():
    customers = customer.query.all()
    return jsonify(
        {
            "success": True,
            "data": [c.dict() for c in customers]
        }
    ), 200

@app.route("/customer/<int:id>", methods=['GET'])
def get_customer(id):
    cust = db.session.get(customer, id)
    if not cust:
        return jsonify(
            {
                "success": False,
                "error": "Customer not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": cust.dict()
        }
    ), 200


@app.route("/customer", methods=['POST'])
def add_customer():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "name", "number", "location"]
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400
            
    try:
        new_customer = customer(
            id=data["id"],
            name=data["name"],
            number=data["number"],
            location=data["location"]
        )
        db.session.add(new_customer)
        db.session.commit()
        
        return jsonify(
            {
                "success": True,
                "data": new_customer.dict()
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



@app.route("/customer/<int:id>", methods=["PUT"])
def update_customer(id):
    cust = db.session.get(customer, id)
    if not cust:
        return jsonify(
            {
                "success": False,
                "error": "Customer not found"
            }
        ), 404
    
    data = request.get_json()
    updatable_fields = ["name", "number", "location"]
    
    for field in updatable_fields:
        if field in data:
            setattr(cust, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": cust.dict()
        }
    ), 200

@app.route("/customer/<int:id>", methods=["DELETE"])
def delete_customer(id):
    cust = db.session.get(customer, id)
    if not cust:
        return jsonify(
            {
                "success": False,
                "error": "Customer not found"
            }
        ), 404
        
    db.session.delete(cust)
    db.session.commit()
    
    return jsonify(
        {
            "success": True,
            "message": "Successfully deleted"
        }
    ), 204
    
    #for experiences table!

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


# for product table!
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








if __name__ == '__main__':
    try:
        # Create tables
        with app.app_context():
            db.create_all()
            print("Database tables created successfully!")
    except Exception as e:
        print(f"Error: {e}")
    
    # Run the app
    app.run(debug=True, port=5001)