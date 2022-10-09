from flask import jsonify

from tavern_db.database import db_session
from tavern_db.models import Relation
from tavern_db.schemas import RelationSchema


def read_all():
    rels = Relation.query.all()

    schema = RelationSchema(many=True)
    return schema.dump(rels)


def read_one(relation_id):
    rel = Relation.query.filter(Relation.id == relation_id).one_or_none()

    if rel is None:
        return jsonify({"msg": f"Relation with id {relation_id} not found."}), 404

    schema = RelationSchema()
    return schema.dump(rel)


def create(body):
    schema = RelationSchema(session=db_session)
    rel = schema.load(body)
    db_session.add(rel)
    db_session.commit()

    return schema.dump(rel)


def update(relation_id, body):
    schema = RelationSchema(partial=True, session=db_session)
    updated_rel = schema.load(body)

    existing_rel = Relation.query.filter(Relation.id == relation_id).one_or_none()
    if existing_rel is None:
        return jsonify({"msg": f"Relation with id {relation_id} not found."}), 404

    updated_rel.id = relation_id
    db_session.merge(updated_rel)
    db_session.commit()

    existing_rel = Relation.query.filter(Relation.id == relation_id).one_or_none()
    return schema.dump(existing_rel)
