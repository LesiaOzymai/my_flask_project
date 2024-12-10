from flask import jsonify, request
from datetime import datetime
from myapp import app
from myapp import database as db

# Define the healthcheck route
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    # Respond with the current status and date
    response = {
        "status": "healthy",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(response), 200
# users
@app.post("/user")
def create_user():
    db.add_user(request.get_json())
    response = {
        "message": "User created",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 201

@app.get("/users")
def get_users():
    return jsonify(db.get_all_users()), 200

@app.get("/user/<int:user_id>")
def get_user(user_id):
    user = db.get_user_by_id(user_id)
    if user:
        return jsonify(user), 200
    return jsonify({"message": "User not found"}), 404

@app.delete("/user/<int:user_id>")
def delete_user(user_id):
    if db.delete_user_by_id(user_id):
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404

# categories
@app.post("/category")
def create_category():
    category = request.get_json()
    db.add_category(category)
    response = {
        "message": "Category created",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 201

@app.get("/category")
def get_categories():
    return jsonify(db.get_all_categories()), 200

@app.delete("/category/<int:category_id>")
def delete_category(category_id):
    if db.delete_category(category_id):
        return jsonify({"message": "Category deleted"}), 200
    return jsonify({"message": "Category not found"}), 404

# records
@app.post("/record")
def create_record():
    record = request.get_json()
    db.add_record(record)
    response = {
        "message": "Record created",
        "date": datetime.today(),
        "status": "ok"
    }
    return jsonify(response), 201

@app.get("/record/<int:record_id>")
def get_record(record_id):
    record = db.get_record_by_id(record_id)
    if record:
        return jsonify(record), 200
    return jsonify({"message": "Record not found"}), 404

@app.delete("/record/<int:record_id>")
def delete_record(record_id):
    if db.delete_record(record_id):
        return jsonify({"message": "Record deleted"}), 200
    return jsonify({"message": "Record not found"}), 404

@app.get("/record")
def get_records():
    user_id = request.args.get("user_id", type=int)
    category_id = request.args.get("category_id", type=int)

    if user_id is None and category_id is None:
        return jsonify({"message": "user_id or category_id is required"}), 400
    records = db.get_records_by_user_and_category(user_id, category_id)
    return jsonify(records), 200