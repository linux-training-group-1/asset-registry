import logging.config

from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify

from utils import mysql_db, jwt_handler, sanitizer, redis_client

load_dotenv()  # load env variables from environment or the .env file
# initialize the logger using logger.conf file's config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('app')

# initialize the flask application
app = Flask(__name__)
search_limit = 10


@app.route('/')
def main():
    # Landing page
    return render_template('index.html')


@app.route('/api/login', methods=['POST'])
def login():
    try:
        body = request.get_json()
        # validate the body
        username = body['username']
        password = body['password']
        if not sanitizer.validate_user_pass(body):
            return jsonify({"message": "Username or password too long"}), 400
        # check password from the database
        result = mysql_db.check_credentials(username, password)
        if not result:
            return jsonify({"message": "Invalid username or password"}), 401
        # generate the token
        resp = {"token": jwt_handler.encode_user(username)}
        # send the token inside the body
        return jsonify(resp), 200
    except Exception as e:
        logger.warning(e)
        return jsonify({"message": "Server Error"}), 502


@app.route('/api/asset', methods=['POST'])
def add_new_asset():
    return ''


@app.route('/api/asset', methods=['GET', 'POST'])
def search_asset():
    # validate credentials
    token = request.headers.get('token')
    # print(token)
    if token is None:
        return jsonify({"message": "Missing token in Header"}), 401
    if not jwt_handler.validate_jwt(token):
        return jsonify({"message": "Invalid token. Please login again"}), 401

    # parse args (Ex: /api/asset?name=Cisco&limit=10)
    # todo sanitize the user inputs
    name = request.args.get('name')
    id = request.args.get('id')
    limit = request.args.get('limit')
    offset = request.args.get('offset')
    if limit is None:
        limit = search_limit
    if offset is None:
        offset = 0
    if not (name or id):
        return jsonify({"message": "At least one of name or id should be present in query string"}), 400
    if name and id:
        return jsonify({"message": "Only one of name or id should be present in query string"}), 400

    results = []
    # search in redis
    if name is not None:
        # zero or more results
        results = redis_client.string_search(name)
    elif id is not None:
        # only one result; ID should be an exact match
        results = redis_client.get_cache_item_json(id)
    if len(results) > 0:
        return jsonify(results), 200

    # search in mysql
    if name is not None:
        results = mysql_db.get_items_by_name(name, limit, offset)
        if len(results) > 0:
            for item in results:
                redis_client.set_cache_item_json(item['name'], item)
    if id is not None:
        results = mysql_db.get_item_by_id(id)
        # send to redis cache
        if len(results) > 0:
            redis_client.set_cache_item_json(id, results[0])

    print(results)
    return jsonify(results), 200


@app.route('/api/report', methods=['GET'])
def gen_report():
    res = redis_client.string_search("hello")
    return ''


@app.route('/api/health', methods=['GET'])
def health():
    return ''

