import logging.config

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from utils import dbconn, jwt_tokens, validator

load_dotenv()  # load env variables from environment or the .env file
# initialize the logger using logger.conf file's config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('app')

# initialize the flask application
app = Flask(__name__)


@app.route('/')
def main():
    # landing page
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    try:
        body = request.get_json()
        # validate the body
        username = body['username']
        password = body['password']
        if not validator.validate_user_pass(body):
            return jsonify({"message": "Username or password too long"}), 400
        # check password from the database
        result = dbconn.check_credentials(username, password)
        if not result:
            return jsonify({"message": "Invalid username or password"}), 401
        # generate the token
        resp = {"token": jwt_tokens.encode_user(username)}
        # send the token inside the body
        return jsonify(resp), 200
    except Exception as e:
        logger.debug(e)
        return jsonify({"message": "Server Error"}), 502


@app.route('/api/asset', methods=['POST'])
def add_new_asset():
    return ''


@app.route('/api/asset', methods=['GET'])
def search_asset():
    return ''


@app.route('/api/report', methods=['GET'])
def gen_report():
    return ''


@app.route('/api/health', methods=['GET'])
def health():
    return ''


if __name__ == "__main__":
    app.run(port=5000, debug=True)
