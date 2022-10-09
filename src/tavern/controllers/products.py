from datetime import datetime

from flask import jsonify

from tavern_db.database import db_session
from tavern_db.models import BtwType, Group, Product, ProductPosition, SalesPrice
from tavern_db.schemas import ProductSchema


def read_all():
    prods = Product.query.all()

    schema = ProductSchema(many=True)
    return schema.dump(prods)


def read_one(product_id):
    prod = Product.query.filter(Product.id == product_id).one_or_none()
    if prod is None:
        return jsonify({"msg": f"Product with id {product_id} not found"}), 404

    schema = ProductSchema()
    return schema.dump(prod)


def create(body):
    name = body.get("name")
    tag = body.get("tag")
    btw_id = body.get("btw_id")
    group_id = body.get("group_id")
    price = body.get("price")

    prod = Product(name=name, tag=tag)
    btw_type = BtwType.query.filter(BtwType.id == btw_id).one_or_none()
    if btw_type is None:
        return jsonify({"msg": f"Btw type with id {btw_id} not found"}), 404
    price = SalesPrice(date_from=datetime.utcnow(), price=price)
    price.btw = btw_type
    prod.sales_prices.append(price)

    pos = ProductPosition(value=0, amount=0)
    prod.product_positions.append(pos)

    group = Group.query.filter(Group.id == group_id).one_or_none()
    if group is None:
        return jsonify({"msg": f"Product group with id {group_id} not found"}), 404
    prod.group = group

    db_session.add(prod)
    db_session.commit()

    schema = ProductSchema()
    return schema.dump(prod), 201


def update(product_id, body):
    name = body.get("name", None)
    tag = body.get("tag", None)
    group_id = body.get("group_id", None)

    prod = Product.query.filter(Product.id == product_id).one_or_none()
    if prod is None:
        return jsonify({"msg": f"Product with id {product_id} not found"}), 404

    if name:
        prod.name = name
    if tag:
        prod.tag = tag
    if group_id:
        group = Group.query.filter(Group.id == group_id).one_or_none()
        if group is None:
            return jsonify({"msg": f"Product group with id {group_id} not found"}), 404
        prod.group = group

    db_session.commit()

    schema = ProductSchema()
    return schema.dump(prod)
