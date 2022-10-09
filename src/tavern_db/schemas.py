from re import L

from marshmallow.fields import Boolean, Integer
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow_sqlalchemy.fields import Nested

from tavern_db.models import (
    BtwType,
    Permission,
    Product,
    ProductPosition,
    Relation,
    SalesPrice,
    User,
    UserGroup,
)


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


class BtwTypeSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = BtwType
        load_instance = True


class SalesPriceSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SalesPrice
        load_instance = True


class ProductPositionSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = ProductPosition
        load_instance = True


class ProductSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = True

    current_price = Nested(SalesPriceSchema, dump_only=True)
    current_position = Nested(ProductPositionSchema, dump_only=True)
