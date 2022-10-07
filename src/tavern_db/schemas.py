from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from tavern_db.models import Permission, User, UserGroup


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
