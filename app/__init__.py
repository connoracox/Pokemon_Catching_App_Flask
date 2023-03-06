from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app,db)
login = LoginManager(app)

login.login_view = 'sign_in'
login.login_message = 'Make sure to login!'

# import routes always at bottom of page
from app import routes, models