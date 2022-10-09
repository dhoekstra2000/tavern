from tavern_db.models import Relation
from tavern_db.schemas import RelationSchema
from tavern_db.database import db_session


def read_all():
    rels = Relation.query.all()

    schema = RelationSchema(many=True)
    return schema.dump(rels)


def create(body):
    schema = RelationSchema(session=db_session)
    rel = schema.load(body)
    db_session.add(rel)
    db_session.commit()

    return schema.dump(rel)
