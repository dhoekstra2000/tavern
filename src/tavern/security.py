from functools import wraps

import jwt
from flask import jsonify, g
from werkzeug.exceptions import Unauthorized

from tavern.config import AppConfig
from tavern_db.models import User


def decode_token(token):
    try:
        decoded_token = jwt.decode(token, AppConfig.SECRET, algorithms=["HS256"])
        user = User.query.filter(User.id == decoded_token["sub"]).first()
        g.user = user
        return decoded_token
    except jwt.PyJWTError as e:
        raise Unauthorized from e


def needs_permission(permission):
    def needs_permission_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwds):
            if g.user.has_permission(permission):
                return f(*args, **kwds)
            return jsonify({"msg": "Insufficient permissions"}), 403
        return wrapper
    return needs_permission_decorator