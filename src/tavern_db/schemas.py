from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested
from marshmallow.fields import Boolean

from tavern_db.models import Permission, Relation, User, UserGroup


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


class PermissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Permission
        load_instance = True


class UserGroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserGroup
        load_instance = True

    permissions = Nested(PermissionSchema, many=True)


class RelationSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Relation
        load_instance = True

    has_budget = Boolean()
