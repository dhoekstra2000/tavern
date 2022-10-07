from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from tavern_db.models import Permission, User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True


class PermissionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Permission
        load_instance = True
