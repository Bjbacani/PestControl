from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

# Initialize Flask app
app = Flask(__name__)

# Secret key to encode the JWT
app.config['JWT_SECRET_KEY'] = 'your_secret_key'  # Change this to a more secure key

# Initialize the JWT Manager
jwt = JWTManager(app)

# Simulate a database with a list of users (replace this with a real DB in production)
users = [
    {"username": "user1", "password": "password1"},
    {"username": "user2", "password": "password2"}
]

# Route for user login and obtaining JWT token
@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    # Check if username and password match any user in the "database"
    user = next((u for u in users if u['username'] == username and u['password'] == password), None)

    if user is None:
        return jsonify({"msg": "Bad username or password"}), 401

    # Create an access token with the user's identity (username)
    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token)

# Protected route that requires a valid JWT token
@app.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Get the identity of the logged-in user from the JWT
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

# Route to check if the server is running
@app.route('/')
def home():
    return jsonify(message="Welcome to the Flask JWT Authentication Example!")

if __name__ == '__main__':
    app.run(debug=True)
