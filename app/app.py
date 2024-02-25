import os

from flask import Flask, jsonify
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv

import config
from app.database.db import db

from flask_cors import CORS

# from app.resources.emails import blp as QueryBlueprint
# from app.resources.users import blp as CommentBlueprint
from app.resources.emails import blp as EmailsBlueprint
from app.resources.users import blp as UsersBlueprint


def create_app(db_url=None):
    app = Flask(__name__)
    CORS(app, origins=["http://192.168.1.6:8080", "http://localhost:8080"])
    load_dotenv()
    app.config.from_object(config.get_config())

    db.init_app(app)

    migrate = Migrate(app, db)

    api = Api(app)

    # app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

    jwt = JWTManager(app)

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {"description": "The token has been revoked.", "error": "token_revoked"}
            ),
            401
        )

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return (
            jsonify({"message": "The token has expired.", "error": "token_expired"}),
            401,
        )

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return (
            jsonify(
                {"message": "Signature verification failed.", "error": "invalid_token"}
            ),
            401,
        )

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return (
            jsonify(
                {
                    "description": "Request does not contain an access token.",
                    "error": "authorization_required",
                }
            ),
            401,
        )

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback(jwt_header, jwt_payload):
        return (
            jsonify(
                {
                    "description": "The token is not fresh.",
                    "error": "fresh_token_required",
                }
            ),
            401,
        )

    api.register_blueprint(UsersBlueprint)
    api.register_blueprint(EmailsBlueprint)

    return app
