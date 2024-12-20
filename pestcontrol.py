from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt
from functools import wraps
from datetime import timedelta
import os

app = Flask(__name__)

# Database configuration

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@127.0.0.1/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# JWT configuration
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'test-key')
app.config['JWT_IDENTITY_CLAIM'] = 'sub'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False
jwt = JWTManager(app)

db = SQLAlchemy(app)

# Role-based access control decorator
def role_required(roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get('role') not in roles:
                return jsonify({'error': 'Unauthorized'}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

# Add login route
@app.route('/login', methods=['POST'])
def login():
  
    username = request.json.get('username')
    password = request.json.get('password')
    
    # Mock user verification (replace with your actual user verification)
    if username == 'admin' and password == 'admin123':
        access_token = create_access_token(
            identity='admin', additional_claims={'role': 'admin'}
        )
        return jsonify({'token': access_token}), 200
    elif username == 'user' and password == 'user123':
        access_token = create_access_token(
             identity='user', additional_claims={'role': 'user'}
        )
        return jsonify({'token': access_token}), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401



class customer(db.Model):
    __tablename__ = 'customer'
    id = db.Column(db.Integer, primary_key=True ,autoincrement=True )
    fname = db.Column(db.String(45), nullable=False)
    Lastname = db.Column(db.String(45), nullable=False)
    contact = db.Column(db.String(45), nullable=False)
    Location = db.Column(db.String(45), nullable=False)
    
    def dict(self):
        return {
            "id": self.id,
            "fname": self.fname,
            "Lastname": self.Lastname,
            "contact": self.contact,
            "Location": self.Location
        }

# Add these route handlers
@app.route("/customer", methods=["GET"])
@jwt_required()
@role_required(['admin', 'user'])
def get_customers():
    customers = customer.query.all()
    return jsonify(
        {
            "success": True,
            "data": [c.dict() for c in customers]
        }
    ), 200

@app.route("/customer/<int:id>", methods=['GET'])
@jwt_required()
@role_required(['admin', 'user'])
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
@jwt_required()
@role_required(['admin'])
def add_customer():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "fname", "Lastname", "contact", "Location"]
    
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
            fname=data["fname"],
            Lastname=data["Lastname"],
            contact=data["contact"],
            Location=data["Location"]
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
@jwt_required()
@role_required(['admin'])
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
    updatable_fields = ["fname","Lastname", "contact", "Location"]
    
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
@jwt_required()
@role_required(['admin'])
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
    id = db.Column(db.Integer, primary_key=True,autoincrement=True )
    date = db.Column(db.String(45), nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.String(255), nullable=False)
    
    def dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "customer_id": self.customer_id,
            "product_id": self.product_id,
            "experience": self.experience
        }

@app.route("/experiences", methods=["GET"])
@jwt_required()
@role_required(['admin', 'user'])
def get_experiences():
    exp = experiences.query.limit(100)
    return jsonify(
        {
            "success": True,
            "data": [e.dict() for e in exp]
        }
    ), 200

@app.route("/experiences/<int:id>", methods=['GET'])
@jwt_required()
@role_required(['admin', 'user'])
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
@jwt_required()
@role_required(['admin'])
def add_experience():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "date", "customer_id", "product_id", "experience"]
    
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
            customer_id=data["customer_id"],
            product_id=data["product_id"],
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
@jwt_required()
@role_required(['admin'])
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
    updatable_fields = ["date", "customer_id", "product_id", "experience"]
    
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
@jwt_required()
@role_required(['admin'])
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
class product(db.Model):
    __tablename__='product'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True )
    name = db.Column(db.String(45), nullable=False)
    c_method = db.Column(db.String(45), nullable=False)
    c_type = db.Column(db.String(45), nullable=False)
    pest = db.Column(db.String(45), nullable=False)
    
    def dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "c_method": self.c_method,
            "c_type": self.c_type,
            "pest": self.pest
        }

@app.route("/product", methods=["GET"])
@jwt_required()
@role_required(['admin', 'user'])
def get_prod():
    pr = product.query.limit(100)
    return jsonify(
        {
            "success": True,
            "data": [prs.dict() for prs in pr]
        }
    ), 200

@app.route("/product/<int:id>", methods=['GET'])
@jwt_required()
@role_required(['admin', 'user'])
def get_prods(id):
    prs = db.session.get(product, id)
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


@app.route("/product", methods=['POST'])
@jwt_required()
@role_required(['admin'])
def add_prod():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "name", "c_method", "c_type","pest"]
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400
            
    try:
        new_pr = product(
            id=data["id"],
            name=data["name"],
            c_method=data["c_method"],
            c_type=data["c_type"],
            pest=data["pest"]
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

@app.route("/product/<int:id>", methods=["PUT"])
@jwt_required()
@role_required(['admin'])
def update_pr(id):
    prs = db.session.get(product, id)
    if not prs:
        return jsonify(
            {
                "success": False,
                "error": "Product not found"
            }
        ), 404
    
    data = request.get_json()
    updatable_fields = ["name", "c_method","c_type","pest"]
    
    for field in updatable_fields:
        if field in data:
            setattr(prs, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": prs.dict()
        }
    ), 200
    
@app.route("/product/<int:id>", methods=["DELETE"])
@jwt_required()
@role_required(['admin'])
def delete_pr(id):
    prs = db.session.get(product, id)
    if not prs:
        return jsonify(
            {
                "success": False,
                "error": "Product not found"
            }
        ), 404
    
    db.session.delete(prs)
    db.session.commit()
    return jsonify(
        {
            "success": True,
            "message": "Product successfully Deleted"
        }
    ), 204

# for purchase table!

class purchase(db.Model):
    __tablename__='purchase'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True )
    date = db.Column(db.String(45), nullable=False)
    product_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    
    def dict(self):
        return {
            "id": self.id,
            "date": self.date,
            "product_id": self.product_id,
            "customer_id": self.customer_id
        }

@app.route("/purchase", methods=["GET"])
@jwt_required()
@role_required(['admin', 'user'])
def get_purchases():
    purchases = purchase.query.all()
    return jsonify(
        {
            "success": True,
            "data": [p.dict() for p in purchases]
        }
    ), 200

@app.route("/purchase/<int:id>", methods=['GET'])
@jwt_required()
@role_required(['admin', 'user'])
def get_purchase(id):
    purch = db.session.get(purchase, id)
    if not purch:
        return jsonify(
            {
                "success": False,
                "error": "Purchase not found"
            }
        ), 404
    return jsonify(
        {
            "success": True,
            "data": purch.dict()
        }
    ), 200

@app.route("/purchase", methods=['POST'])
@jwt_required()
@role_required(['admin'])
def add_purchase():
    if not request.is_json:
        return jsonify(
            {
                "success": False,
                "error": "Content-type must be application/json"
            }
        ), 400
    data = request.get_json()
    required_fields = ["id", "date", "product_id", "customer_id"]
    
    for field in required_fields:
        if field not in data:
            return jsonify(
                {
                    "success": False,
                    "error": f"Missing field: {field}"
                }
            ), 400
            
    try:
        new_purchase = purchase(
            id=data["id"],
            date=data["date"],
            product_id=data["product_id"],
            customer_id=data["customer_id"]
        )
        db.session.add(new_purchase)
        db.session.commit()
        
        return jsonify(
            {
                "success": True,
                "data": new_purchase.dict()
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

@app.route("/purchase/<int:id>", methods=["PUT"])
@jwt_required()
@role_required(['admin'])
def update_purchase(id):
    purch = db.session.get(purchase, id)
    if not purch:
        return jsonify(
            {
                "success": False,
                "error": "Purchase not found"
            }
        ), 404
    
    data = request.get_json()
    updatable_fields = ["date", "product_id", "customer_id"]
    
    for field in updatable_fields:
        if field in data:
            setattr(purch, field, data[field])

    db.session.commit()
    return jsonify(
        {
            "success": True,
            "data": purch.dict()
        }
    ), 200


@app.route("/purchase/<int:id>", methods=["DELETE"])
@jwt_required()
@role_required(['admin'])
def delete_purchase(id):
    purch = db.session.get(purchase, id)
    if not purch:
        return jsonify(
            {
                "success": False,
                "error": "Purchase not found"
            }
        ), 404
        
    db.session.delete(purch)
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
            #db.create_all()
            print("Database successfully connected!")
    except Exception as e:
        print(f"Error: {e}")
    
    # Run the app with correct port
    app.run(debug=True, port=5009)