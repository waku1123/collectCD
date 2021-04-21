from . import db
import datetime
from marshmallow import fields, Schema
from typing import Dict


class Collection(db.Model):
    """
    Collection Model
    """

    __tablename__ = "collections"

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey("albums.id"), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, data: Dict):
        self.album_id = data.get("album_id")
        self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
        self.updated_at = datetime.datetime.now()
        db.session.commit()

    @staticmethod
    def get_all_collections():
        return Collection.query.all()

    @staticmethod
    def get_one_collection(id_: int):
        return Collection.query.get(id_)

    def __repr__(self):
        return f"<id {self.id}>"


class CollectionSchema(Schema):
    """
    Collection Schema
    """

    id = fields.Int(dump_only=True)
    album_id = fields.Int(dump_only=True, required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
