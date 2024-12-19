#views.py
from datetime import datetime
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import text
from myapp.models import db, Accounts
from myapp.schemas import *
from myapp import lab2_database as lb_db

views = Blueprint("views", __name__)

# Initialize schemas
user_sch = UserSch()
category_sch = CategorySch()
record_sch = RecordSch()
account_sch = AccountSch()
funds_sch = FundsSch()

# Define a single healthcheck route
@views.route('/healthcheck', methods=['GET'])
def healthcheck():
    """
    Healthcheck route to verify the application is running
    """
    return response_message("Healthcheck is running")


# Users endpoints
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
def get_user(user_id):
    user = lb_db.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404


@views.delete("/user/<int:user_id>")
def delete_user(user_id):
    if lb_db.delete_user_by_id(user_id):
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404


# Categories endpoints
@views.post("/category")
def create_category():
    category = request.get_json()
    lb_db.add_category(category)
    return response_message("Category created"), 201


@views.get("/category")
def get_categories():
    return jsonify(lb_db.get_all_categories()), 200


@views.delete("/category/<int:category_id>")
def delete_category(category_id):
    if lb_db.delete_category(category_id):
        return jsonify({"message": "Category deleted"}), 200
    return jsonify({"message": "Category not found"}), 404


# Records endpoints
@views.post("/record")
def create_record():
    record = request.get_json()
    lb_db.add_record(record)
    return response_message("Record created"), 201


@views.get("/record/<int:record_id>")
def get_record(record_id):
    record = lb_db.get_record_by_id(record_id)
    if record:
        return jsonify(record), 200
    return jsonify({"message": "Record not found"}), 404


@views.delete("/record/<int:record_id>")
def delete_record(record_id):
    if lb_db.delete_record(record_id):
        return jsonify({"message": "Record deleted"}), 200
    return jsonify({"message": "Record not found"}), 404


@views.get("/record")
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


def validate_request(schema, payload):
    errors = schema.validate(payload)
    if errors:
        return errors, 400
    return None, None


# Accounts endpoints
@views.post("/accounts/create")
def create_account():
    data = request.get_json()
    errors, status = validate_request(account_sch, data)
    if errors:
        return jsonify(errors), status

    try:
        account = Accounts(user_id=data['user_id'], balance=data.get('balance', 0.0))
        db.session.add(account)
        db.session.commit()
        return response_message("Account created", data=account_sch.dump(account)), 201
    except IntegrityError:
        db.session.rollback()
        return response_message("User already has an account", "error"), 400


@views.post("/accounts/add-funds")
def add_funds():
    data = request.get_json()
    errors, status = validate_request(funds_sch, data)
    if errors:
        return jsonify(errors), status

    account = Accounts.query.filter_by(user_id=data['user_id']).first()
    if not account:
        return response_message("Account not found", "error"), 404

    account.balance += data['amount']
    db.session.commit()
    return response_message("Funds added", data={"balance": account.balance}), 200


@views.get("/accounts")
def get_all_accounts():
    accounts = Accounts.query.all()
    if not accounts:
        return response_message("No accounts found", "error"), 404
    return jsonify(account_sch.dump(accounts, many=True)), 200


@views.get("/accounts/user/<int:user_id>")
def get_account_by_user_id(user_id):
    account = Accounts.query.filter_by(user_id=user_id).first()
    if not account:
        return response_message("Account not found", "error"), 404
    return jsonify(account_sch.dump(account)), 200


@views.delete("/accounts/user")
def delete_account():
    data = request.get_json()
    user_id = data.get("user_id")

    account = Accounts.query.filter_by(user_id=user_id).first()
    if not account:
        return response_message("Account not found", "error"), 404

    db.session.delete(account)
    db.session.commit()
    return response_message("Account deleted"), 200


@views.post("/expenses")
def create_expense():
    data = request.get_json()
    errors, status = validate_request(funds_sch, data)
    if errors:
        return jsonify(errors), status

    account = Accounts.query.filter_by(user_id=data['user_id']).first()
    if not account:
        return response_message("Account not found", "error"), 404

    if account.balance < data['amount']:
        return response_message("Insufficient funds", "error"), 400

    account.balance -= data['amount']
    db.session.commit()
    return response_message("Expense created", data={"balance": account.balance}), 201


# Database Health Check
@views.get("/dbcheck")
def db_check():
    try:
        db.session.execute(text("SELECT 1"))
        return response_message("Database connection is healthy"), 200
    except Exception as e:
        return response_message("Database connection failed", "error", str(e)), 500