import time

import jwt
from flask import jsonify
from passlib.hash import pbkdf2_sha256

from tavern.config import AppConfig
from tavern_db.database import db_session
from tavern_db.models import User
from tavern_db.schemas import UserSchema


def read_all():
    users = User.query.all()

    schema = UserSchema(
        only=["id", "username", "date_created", "date_updated"], many=True
    )
    return schema.dump(users)


def read_one_by_id(user_id):
    user = User.query.filter(User.id == user_id).one_or_none()
    if user is None:
        return jsonify({"msg": f"User with ID {user_id} not found"}), 404
    else:
        schema = UserSchema(only=["id", "username", "date_created", "date_updated"])
        return schema.dump(user)


def read_one_by_username(username):
    user = User.query.filter(User.username == username).one_or_none()
    if user is None:
        return jsonify({"msg": f"User with ID {username} not found"}), 404
    else:
        schema = UserSchema(only=["id", "username", "date_created", "date_updated"])
        return schema.dump(user)


def create(body):
    username = body.get("username")
    password = body.get("password")

    existing_user = User.query.filter(User.username == username).one_or_none()
    if existing_user is not None:
        return jsonify({"msg": f"User with username {username} already exists."}), 409

    hash = pbkdf2_sha256.hash(password)
    user = User(username=username, password=hash)
    db_session.add(user)
    db_session.commit()

    schema = UserSchema(only=["id", "username", "date_created", "date_updated"])
    return schema.dump(user), 201


def update_by_id(user_id, body):
    password = body.get("password")

    user = User.query.filter(User.id == user_id).one_or_none()
    if user is None:
        return jsonify({"msg": f"User with ID {user_id} not found"}), 404

    user.password = pbkdf2_sha256.hash(password)
    db_session.commit()

    schema = UserSchema(only=["id", "username", "date_created", "date_updated"])
    return schema.dump(user)


def update_by_username(username, body):
    password = body.get("password")

    user = User.query.filter(User.username == username).one_or_none()
    if user is None:
        return jsonify({"msg": f"User with ID {username} not found"}), 404

    user.password = pbkdf2_sha256.hash(password)
    db_session.commit()

    schema = UserSchema(only=["id", "username", "date_created", "date_updated"])
    return schema.dump(user)


def _current_timestamp() -> int:
    return int(time.time())


def authenticate(body):
    username = body.get("username")
    password = body.get("password")

    user = User.query.filter(User.username == username).one_or_none()
    if user is not None and pbkdf2_sha256.verify(password, user.password):
        timestamp = _current_timestamp()
        payload = {"iat": int(timestamp), "exp": int(timestamp + 600), "sub": user.id}
        token = jwt.encode(payload, AppConfig.SECRET)
        return jsonify({"token": token})
    else:
        return jsonify({"msg": "Authentication failed"}), 401
