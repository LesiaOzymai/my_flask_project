#config.py
import os

PROPAGATE_EXCEPTIONS = True
FLASK_DEBUG = True
SQLALCHEMY_DATABASE_URI = f'postgresql://{os.environ.get("POSTGRES_USER", "default_user")}:{os.environ.get("POSTGRES_PASSWORD", "default_password")}@{os.environ.get("DB_HOST", "localhost")}/{os.environ.get("POSTGRES_DB", "default_db")}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_default_key_here")
API_TITLE = "Finance REST API"
API_VERSION = "v1"
OPENAPI_VERSION = "3.0.3"
OPENAPI_URL_PREFIX = "/"
OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"