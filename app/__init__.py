from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret"  # для расширений Flask
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    CORS(app)   # разрешаем кросс-доменные запросы
    db.init_app(app)

    # регистрация роутов
    from .routes import bp
    app.register_blueprint(bp, url_prefix="/api")

    # создание таблиц
    with app.app_context():
        db.create_all()

    return app