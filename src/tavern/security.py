import jwt
from werkzeug.exceptions import Unauthorized

from tavern.config import AppConfig


def decode_token(token):
    try:
        decoded_token = jwt.decode(token, AppConfig.SECRET, algorithms=["HS256"])
        return decoded_token
    except jwt.PyJWTError as e:
        raise Unauthorized from e
