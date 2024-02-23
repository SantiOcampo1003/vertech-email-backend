from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

import config
from app.database import db

def create_app(db_url=None):
    # Load environment variables first
    load_dotenv()

    app = Flask(__name__)
    # Configure the app using the Config class
    app.config.from_object(config.get_config())

    db.init_app(app)

    return app
