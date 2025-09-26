from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap5 import Bootstrap
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)
Bootstrap(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
