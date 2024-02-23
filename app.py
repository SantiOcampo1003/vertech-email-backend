from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from flask_smorest import Api

import config
from app.database import db

def create_app(db_url=None):
    # Load environment variables first
    load_dotenv()

    app = Flask(__name__)
    # Configure the app using the Config class
    app.config.from_object(config.get_config())

    db.init_app(app)
    api = Api(app)


    with app.app_context():
        import app.models
        db.create_all()

    return app