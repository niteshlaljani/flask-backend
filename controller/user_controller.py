from app import app
from model.user_model import User, engine
from flask import request, jsonify
from sqlalchemy.orm import sessionmaker

# Setup the session
Session = sessionmaker(bind=engine)
session = Session()

def _build_cors_preflight_response():
    response = jsonify()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response

def validate_user_data(data):
    required_fields = ['name', 'number', 'role', 'email', 'password']
    for field in required_fields:
        if field not in data or not data[field]:
            return f"{field} is required"
    
    if len(data['number']) != 10 or not data['number'].isdigit():
        return "Phone number must be a 10-digit number"
    
    if data['role'] not in ['user', 'admin']:
        return "Role must be either 'user' or 'admin'"
    
    return None

@app.route("/user", methods=["POST"])
def create():
    try:
        data = request.json  # Handle JSON data
        error_message = validate_user_data(data)
        if error_message:
            return jsonify({"error": error_message}), 400
        
        name = data['name']
        number = data['number']
        role = data['role']
        email = data['email']
        password = data['password']
        user = User(name=name, number=number, role=role, email=email, password=password)
        session.add(user)
        session.commit()
        return jsonify({"message": "User created successfully", "user": {"name": user.name, "number": user.number, "email": user.email, "role": user.role, "password": user.password}}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/user/login", methods=["POST"])
def login():
    try:
        data = request.json  # Handle JSON data
        email = data.get('email')
        password = data.get('password')
        print("email & password received", email, password)

        if email and password:
            user = session.query(User).filter_by(email=email, password=password).first()
            if user:
                return jsonify({"name": user.name, "number": user.number, "email": user.email, "role": user.role, "password": user.password}), 200
            return jsonify({"error": "User not found or invalid credentials"}), 404
        else:
            return jsonify({"error": "Email and password are required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/user", methods=["GET"])
def read():
    try:
        users = session.query(User).all()
        users_list = [{"id": user.id, "name": user.name, "number": user.number, "email": user.email, "role": user.role, "password": user.password} for user in users]
        return jsonify(users_list), 200
    except Exception as e:
        return jsonify({"error": str(e), "message": "error retrieving users"}), 500

@app.route("/user", methods=["PUT"])
def update():
    try:
        data = request.json  # Handle JSON data
        email = data.get('email')
        password = data.get('password')
        user = session.query(User).filter_by(email=email, password=password).first()
        if user:
            name = data.get('name')
            number = data.get('number')
            role = data.get('role')
            new_password = data.get('new_password')

            if name:
                user.name = name
            if number:
                if len(number) != 10 or not number.isdigit():
                    return jsonify({"error": "Phone number must be a 10-digit number"}), 400
                user.number = number
            if role:
                if role not in ['user', 'admin']:
                    return jsonify({"error": "Role must be either 'user' or 'admin'"}), 400
                user.role = role
            if new_password:
                user.password = new_password

            session.commit()
            return jsonify({"message": "User updated successfully", "user": {"name": user.name, "number": user.number, "email": user.email, "role": user.role}}), 200
        return jsonify({"error": "User not found or invalid credentials"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/user", methods=["DELETE"])
def delete():
    try:
        data = request.json  # Handle JSON data
        email = data.get('email')
        password = data.get('password')
        user = session.query(User).filter_by(email=email, password=password).first()
        if user:
            session.delete(user)
            session.commit()
            return jsonify({"message": "User deleted successfully"}), 204
        return jsonify({"error": "User not found or invalid credentials"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET,POST,PUT,DELETE,OPTIONS")
    return response
