from flask import jsonify
from datetime import datetime
from myapp import app

# Define the healthcheck route
@app.route('/healthcheck', methods=['GET'])
def healthcheck():
    # Respond with the current status and date
    response = {
        "status": "healthy",
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    return jsonify(response), 200