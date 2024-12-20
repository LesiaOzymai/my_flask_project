#views.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
from passlib.hash import pbkdf2_sha256
from myapp.models import db, Accounts
from myapp.schemas import *
from datetime import datetime
from myapp import lab2_database as lb_db

views = Blueprint("views", __name__)

# Initialize schemas
user_sch = UserSch()
category_sch = CategorySch()
record_sch = RecordSch()
account_sch = AccountSch()
funds_sch = FundsSch()

# Authentication Endpoints
@views.post("/register")
def register():
    user_data = request.get_json()
    hashed_password = pbkdf2_sha256.hash(user_data["password"])
    user = Accounts(user_id=user_data["user_id"], password=hashed_password, balance=0.0)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201

@views.post("/login")
def login():
    user_data = request.get_json()
    user = Accounts.query.filter_by(user_id=user_data["user_id"]).first()
    if user and pbkdf2_sha256.verify(user_data["password"], user.password):
        access_token = create_access_token(identity=user.user_id)
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

# Example of a protected endpoint
@views.get("/protected")
@jwt_required()
def protected():
    return jsonify({"message": "You are viewing a protected route"}), 200

# Existing Users Endpoints
@views.post("/user")
def create_user():
    lb_db.add_user(request.get_json())
    response = {
        "message": "User created",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "ok"
    }
    return jsonify(response), 201

@views.get("/users")
def get_users():
    return jsonify(lb_db.get_all_users()), 200

@views.get("/user/<int:user_id>")
@jwt_required()  # Protect this endpoint
def get_user(user_id):
    user = lb_db.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404

@views.delete("/user/<int:user_id>")
@jwt_required()  # Protect this endpoint
def delete_user(user_id):
    if lb_db.delete_user_by_id(user_id):
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404

# Existing Categories Endpoints
@views.post("/category")
@jwt_required()  # Protect this endpoint
def create_category():
    category = request.get_json()
    lb_db.add_category(category)
    return response_message("Category created"), 201

@views.get("/category")
@jwt_required()  # Protect this endpoint
def get_categories():
    return jsonify(lb_db.get_all_categories()), 200

@views.delete("/category/<int:category_id>")
@jwt_required()  # Protect this endpoint
def delete_category(category_id):
    if lb_db.delete_category(category_id):
        return jsonify({"message": "Category deleted"}), 200
    return jsonify({"message": "Category not found"}), 404

# Existing Records Endpoints
@views.post("/record")
@jwt_required()  # Protect this endpoint
def create_record():
    record = request.get_json()
    lb_db.add_record(record)
    return response_message("Record created"), 201

@views.get("/record/<int:record_id>")
@jwt_required()  # Protect this endpoint
def get_record(record_id):
    record = lb_db.get_record_by_id(record_id)
    if record:
        return jsonify(record), 200
    return jsonify({"message": "Record not found"}), 404

@views.delete("/record/<int:record_id>")
@jwt_required()  # Protect this endpoint
def delete_record(record_id):
    if lb_db.delete_record(record_id):
        return jsonify({"message": "Record deleted"}), 200
    return jsonify({"message": "Record not found"}), 404

@views.get("/record")
@jwt_required()  # Protect this endpoint
def get_records():
    user_id = request.args.get("user_id", type=int)
    category_id = request.args.get("category_id", type=int)

    if user_id is None and category_id is None:
        return jsonify({"message": "user_id or category_id is required"}), 400

    records = lb_db.get_records_by_user_and_category(user_id, category_id)
    return jsonify(records), 200

# Helper functions
def response_message(message, status="ok", data=None):
    return jsonify({
        "message": message,
        "status": status,
        "data": data,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })