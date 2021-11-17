from cerberus import Validator
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from utils import dbconn, jwt_tokens

load_dotenv()  # load env variables from environment or the .env file
# from flask_mysqldb import MySQL

# mysql = MySQL()
app = Flask(__name__)


## MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = 'jay'
# app.config['MYSQL_DATABASE_PASSWORD'] = 'jay'
# app.config['MYSQL_DATABASE_DB'] = 'BucketList'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)


@app.route('/')
def main():
    # landing page
    return render_template('index.html')


@app.route('/login', methods=['POST'])
def login():
    body = request.get_json()
    # validate the body
    schema = {'username': {'type': 'string', 'maxlength': 255},
              "password": {'type': 'string', 'maxlength': 255}}
    validator = Validator(schema)
    if not validator.validate(body):
        return jsonify({"message": "Username or password too long"}), 400
    # check password from the database
    result = dbconn.check_credentials(body['username'], body['password'])
    if not result:
        return jsonify({"message": "Invalid username or password"}), 401
    # generate the token
    resp = {"token": jwt_tokens.encode_user(body['username'])}
    # send the token inside the body
    return jsonify(resp), 200


@app.route('/asset', methods=['POST'])
def add_new_asset():
    return ''


@app.route('/asset', methods=['GET'])
def search_asset():
    return ''


@app.route('/report', methods=['GET'])
def gen_report():
    return ''


@app.route('/health', methods=['GET'])
def health():
    return ''


if __name__ == "__main__":
    app.run(port=5000, debug=True)
