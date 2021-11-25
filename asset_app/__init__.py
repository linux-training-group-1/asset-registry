from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
import os

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.environ['MYSQL_USER'] + ":" + os.environ[
    'MYSQL_PASSWORD'] + "@" + os.environ['MYSQL_HOST'] + ":" + os.environ['MYSQL_PORT'] + "/" + os.environ['MYSQL_DB']

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "home_page"

from asset_app import routes
