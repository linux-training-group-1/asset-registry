import datetime
from datetime import timezone
import uuid

import jwt
import os

token_valid_days = 30
encode_algo = "HS256"


def current_time():
    return datetime.datetime.now(tz=timezone.utc).timestamp()


def exp_time():
    return datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=token_valid_days)


def encode_user(username):
    payload = {
        "iss": "asset-app",
        "sub": username,
        "aud": ["all"],
        "iat": current_time(),
        "nbf": current_time(),
        "exp": exp_time(),
        "jti": str(uuid.uuid4()),
        "context": {
            "username": username,
            "roles": ["admin"]
        }
    }
    return jwt.encode(payload=payload, key=os.environ['JWT_SECRET'], algorithm=encode_algo)
