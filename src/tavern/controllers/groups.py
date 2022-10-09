from flask import jsonify

from tavern_db.database import db_session
from tavern_db.models import Group
from tavern_db.schemas import GroupSchema


def read_all():
    groups = Group.query.all()

    schema = GroupSchema(many=True)
    return schema.dump(groups)


def read_one(group_id):
    group = Group.query.filter(Group.id == group_id).one_or_none()
    if group is None:
        return jsonify({"msg": f"Product group with id {group_id} not found."}), 404

    schema = GroupSchema()
    return schema.dump(group)


def create(body):
    name = body.get("name")

    group = Group(name=name)
    db_session.add(group)
    db_session.commit()

    schema = GroupSchema()
    return schema.dump(group), 201


def update(group_id, body):
    name = body.get("name")

    group = Group.query.filter(Group.id == group_id).one_or_none()
    if group is None:
        return jsonify({"msg": f"Product group with id {group_id} not found."}), 404

    if name:
        group.name = name
        db_session.commit()

    schema = GroupSchema()
    return schema.dump(group)
