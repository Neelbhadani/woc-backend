import os
from flask import Flask
from app.extensions import mongo, mail


def create_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = os.getenv("MONGO_URI", "mongodb://localhost:27017/woc")
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    app.config["BASE_URL"] = os.getenv("BASE_URL")
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT"))
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USE_SSL'] = False

    mongo.init_app(app)
    mail.init_app(app)

    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/api')

    return app
