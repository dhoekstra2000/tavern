from flask import jsonify

from tavern_db.database import db_session
from tavern_db.models import BtwType
from tavern_db.schemas import BtwTypeSchema


def read_all():
    btw_types = BtwType.query.all()

    schema = BtwTypeSchema(many=True)
    return schema.dump(btw_types)


def read_one(btw_id):
    btw_type = BtwType.query.filter(BtwType.id == btw_id).one_or_none()
    if btw_type is None:
        return jsonify({"msg": f"Btw type with id {btw_id} not found."}), 404

    schema = BtwTypeSchema()
    return schema.dump(btw_type)


def create(body):
    schema = BtwTypeSchema(session=db_session)
    new_btw = schema.load(body)
    db_session.add(new_btw)
    db_session.commit()

    return schema.dump(new_btw)


def update(btw_id, body):
    schema = BtwTypeSchema(session=db_session, partial=True)
    up_btw = schema.load(body)

    btw_type = BtwType.query.filter(BtwType.id == btw_id).one_or_none()
    if btw_type is None:
        return jsonify({"msg": f"Btw type with id {btw_id} not found."}), 404

    up_btw.id = btw_id
    db_session.merge(up_btw)
    db_session.commit()

    btw_type = BtwType.query.filter(BtwType.id == btw_id).one_or_none()
    return schema.dump(btw_type)
