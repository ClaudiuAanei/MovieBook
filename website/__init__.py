import os
from dotenv import find_dotenv, load_dotenv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap5

PATH = find_dotenv()
load_dotenv(PATH)

db = SQLAlchemy()
DB_NAME = "database_moviebook.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv("APP_CONFIG")
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    Bootstrap5(app)

    from .views import views
    from .auth import auth
    from .admin import admin

    app.register_blueprint(views, url_prefix= '/')
    app.register_blueprint(auth, url_prefix= '/')
    app.register_blueprint(admin, url_prefix= '/')

    from .models import User, PopularMovies, RandomMovie, PopularSeries, SaveMovie

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.get_or_404(User, user_id)

    return app

def create_database(app):
    if not os.path.exists(DB_NAME):
        with app.app_context():
            db.create_all()
