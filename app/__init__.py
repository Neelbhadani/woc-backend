import os
from flask import Flask
from app.extensions import mongo, mail


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/woc")

    mongo.init_app(app)
    mail.init_app(app)

    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')

    return app
