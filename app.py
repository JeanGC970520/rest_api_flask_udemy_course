
import os

from flask import Flask
from flask_smorest import Api

import models  # Its necessary import the Models before init SQLAlchemy
from db import db
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

# Applying Factory pattern to build a Flask app
def create_app(db_url=None):
    app = Flask(__name__)

    # Configurations 
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_ULR_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app) # Init our Flask app to connect it with SQLAlchemy

    # Connect Flask app to flask_smorest extension
    api = Api(app)

    # When the app is created, tell SQLAlchemy to create all the database tables we need.
    with app.app_context():
        db.create_all()

    # Registering our Blueprints objects
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)

    return app