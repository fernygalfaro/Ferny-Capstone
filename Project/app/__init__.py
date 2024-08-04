
from flask import Flask
from pymongo import MongoClient


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    # Initialize MongoDB
    mongo_client = MongoClient(app.config['MONGO_URI'])
    app.db = mongo_client.get_database()

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.login import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
