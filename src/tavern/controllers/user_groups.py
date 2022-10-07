from flask import jsonify

from tavern.security import needs_permission
from tavern_db.database import db_session
from tavern_db.models import Permission, UserGroup
from tavern_db.schemas import UserGroupSchema


@needs_permission("Groups | can list groups")
def read_all():
    groups = UserGroup.query.all()

    schema = UserGroupSchema(many=True)
    return schema.dump(groups)


def create(body):
    name = body.get("name")
    permissions = body.get("permissions")

    existing_group = UserGroup.query.filter(UserGroup.name == name).one_or_none()
    if existing_group is not None:
        return jsonify({"msg": f"Group with name {name} already exists."}), 409

    perms = [
        Permission.query.filter(Permission.id == id).one_or_none() for id in permissions
    ]
    perms = [perm for perm in perms if perm is not None]

    group = UserGroup(name=name)
    group.permissions = perms
    db_session.add(group)
    db_session.commit()

    schema = UserGroupSchema()
    return schema.dump(group), 201
