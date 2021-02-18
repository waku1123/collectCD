from marshmallow import fields, Schema
import datetime
from . import db
from ..app import bcrypt
from .Album import AlbumSchema


class Artist(db.Model):
    """
    Artist Model
    """

    __tablename__ = "artists"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    albums = db.relationship("Album", backref="artists", lazy=True)

    def __init__(self, data):
        self.name = data.get("name")
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

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_artists():
        return Artist.query.all()

    @staticmethod
    def get_one_artist(id_: int):
        return Artist.query.get(id_)

    def __repr(self):
        return f"<id {self.id}>"


class ArtistSchema(Schema):
    """
    Artist Schema
    """

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    albums = fields.Nested(AlbumSchema, many=True)
