#__init__.py
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from myapp.models import db
import os


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py', silent=True)
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Змінна середовища
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt = JWTManager(app)

    # Обробники помилок JWT
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return jsonify({"message": "The token has expired.", "error": "token_expired"}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return jsonify({"message": "Signature verification failed.", "error": "invalid_token"}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return jsonify({
            "description": "Request does not contain an access token.",
            "error": "authorization_required"
        }), 401

    from myapp.views import views
    app.register_blueprint(views)
    return app


app = create_app()