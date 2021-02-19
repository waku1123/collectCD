from . import db
import datetime
from marshmallow import fields, Schema
from typing import Dict


class Album(db.Model):
    """
    Album Model
    """

    __tablename__ = "albums"

    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey("artists.id"), nullable=False)
    order = db.Column(db.Integer)
    name = db.Column(db.Integer, nullable=False)
    publish_year = db.Column(db.Integer)
    publish_month = db.Column(db.Integer)
    posession = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    def __init__(self, data: Dict):
        self.artist_id = data.get("artist_id")
        self.order = data.get("order")
        self.name = data.get("name")
        self.publish_year = data.get("publish_year")
        self.publish_month = data.get("publish_month")
        self.posession = data.get("posession")
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
    def get_all_albums():
        return Album.query.all()

    @staticmethod
    def get_one_album(id_: int):
        return Album.query.get(id_)

    def __repr__(self):
        return f"<id {self.id}>"


class AlbumSchema(Schema):
    """
    Album Schema
    """

    id = fields.Int(dump_only=True)
    artist_id = fields.Int(dump_only=True, required=True)
    order = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    publish_year = fields.Int(dump_only=True)
    publish_month = fields.Int(dump_only=True)
    posession = fields.Boolean(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
