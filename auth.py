from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from datetime import timedelta

import os

app = Flask(__name__)
# JWT configuration
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'test-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Mock user database
users_db = {
    'admin': {
        'password': bcrypt.generate_password_hash('admin123').decode('utf-8'),
        'role': 'admin'
    },
    'user': {
        'password': bcrypt.generate_password_hash('user123').decode('utf-8'),
        'role': 'user'
    }
}

@app.route('/login', methods=['POST'])
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Missing credentials'}), 400
    
    user = users_db.get(username)
    if not user or not bcrypt.check_password_hash(user['password'], password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    access_token = create_access_token(
        identity={'username': username, 'role': user['role']}
    )
    return jsonify({'token': access_token}), 200

if __name__ == '__main__':
    app.run(port=5000)