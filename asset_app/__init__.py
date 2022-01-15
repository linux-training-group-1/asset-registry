import logging.config
import os

from dotenv import load_dotenv
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
import redis

logging.config.fileConfig('logging.conf')
logger = logging.getLogger('app')
load_dotenv()
app = Flask(__name__)

# redis config
redis_client = redis.Redis(host=os.environ['REDIS_HOST'],port=os.environ['REDIS_PORT'])


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + os.environ['MYSQL_USER'] + ":" + os.environ[
    'MYSQL_PASSWORD'] + "@" + os.environ['MYSQL_HOST'] + ":" + os.environ['MYSQL_PORT'] + "/" + os.environ['MYSQL_DATABASE']

# app.config['SQLALCHEMY_BINDS']={'one':'mysql+pymysql://' + os.environ['MYSQL_USER'] + ":" + os.environ[
#     'MYSQL_PASSWORD'] + "@" + os.environ['MYSQL_HOST_1'] + ":" + os.environ['MYSQL_PORT'] + "/" + os.environ['MYSQL_DATABASE'],'two':'mysql+pymysql://' + os.environ['MYSQL_USER'] + ":" + os.environ[
#     'MYSQL_PASSWORD'] + "@" + os.environ['MYSQL_HOST_2'] + ":" + os.environ['MYSQL_PORT'] + "/" + os.environ['MYSQL_DATABASE']}   

db = SQLAlchemy(app)

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_POOL_RECYCLE']=30

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "home_page"

from asset_app import routes
