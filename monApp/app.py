from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object("config")

db = SQLAlchemy(app)

from flask_bootstrap5 import Bootstrap
Bootstrap(app)

from flask_login import LoginManager
login_manager = LoginManager(app)
login_manager.login_view = " login"