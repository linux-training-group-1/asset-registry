from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
db= SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://asset-app:akjgSDf#69@34.132.179.103/assets_db'
app.config['SECRET_KEY']='bff4eb94deb028b293786461'
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view="home_page"



from asset_app import routes

