import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_caching import Cache
from flask_injector import FlaskInjector

from .config import Config

db = SQLAlchemy()
bcrypt = Bcrypt()
cache = Cache(config={'CACHE_TYPE': 'SimpleCache'})

# Ensure tensorflow only run on CPU for inference
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
print("\n[INFO] USING CPU FOR TENSORFLOW\n")


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SECRET_KEY'] = Config.SECRET_KEY
    db.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)

    from . import auth
    from . import views

    app.register_blueprint(views.bp, url_prefix='/')
    app.register_blueprint(auth.bp, url_prefix='/')

    create_database(app)

    login_manager = LoginManager(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .dependencies import configure

    # Setup Flask injector for Recommendation Model
    # Referring https://levelup.gitconnected.com/python-dependency-injection-with-flask-injector-50773d451a32
    # NOTE: for some reason FlaskInjector does not work with Flask 2.0
    FlaskInjector(app=app, modules=[configure])

    return app


def create_database(app):
    # IT SEEMS LIKE YOU CAN JUST KEEP CREATING DB in production mode
    #  and still won't overwrite the initially created docker volume.
    # The only way to reset the database is by removing the mounted
    #  docker volume.
    if not os.path.exists(os.path.join('website', Config.DB_NAME)):
        db.create_all(app=app)
        print('\n[INFO] Created Database!!!\n')
