# app/__init__.py

# third-party imports
from flask import Flask
#from flask_sqlalchemy import SQLAlchemy

# local imports
from config import app_config
from flask_login import LoginManager
#from flask_migrate import Migrate
from flask_bootstrap import Bootstrap
from testdynamo import DynamoHelper
# db variable initialization
# update here to dynamodb
from flask_mail import Mail

db = DynamoHelper()
login_manager = LoginManager()
app = Flask(__name__, instance_relative_config=True)
mail=Mail()
def create_app(config_name):

    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')

    Bootstrap(app)
    mail=Mail(app)
    # create table for dynamodb
    # db.init_app(app)

    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"


    # not required anymore
    # migrate = Migrate(app, db)
    if "Employee" not in db.listTables():
        db.createTable("Employee", test=True)


    from app import models

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .home import home as home_blueprint
    app.register_blueprint(home_blueprint)

    return app
