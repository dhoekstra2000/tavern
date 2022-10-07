from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from tavern_db.models import User


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
