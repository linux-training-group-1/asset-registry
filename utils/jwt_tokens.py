import datetime
import json
from datetime import timezone
import uuid

import jwt
import os

token_valid_days = 30
encode_algo = "HS256"


def current_time():
    return int(datetime.datetime.now(tz=timezone.utc).timestamp())


def exp_time():
    return int((datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=token_valid_days)).timestamp())


def encode_user(username):
    payload = {
        "iss": "asset-app",
        "sub": username,
        "aud": "http://localhost",
        "iat": current_time(),
        "nbf": current_time(),
        "exp": exp_time(),
        "jti": str(uuid.uuid4()),
    }
    return jwt.encode(payload=payload, key=os.environ['JWT_SECRET'], algorithm=encode_algo)


def validate_jwt(token):
    # todo verify jwt signature
    return jwt.decode(token, key=os.environ['JWT_SECRET'], algorithms=encode_algo, options={"verify_signature": False})
