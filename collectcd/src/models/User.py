from marshmallow import fields, Schema
import datetime
from . import db
from typing import Dict, List
from ..app import bcrypt


class User(db.Model):
    """
    User Model
    """

    # table name
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

    # class constructor
    def __init__(self, data: Dict):
        """
        Class constructor
        """
        self.name = data.get("name")
        self.email = data.get("email")
        self.password = self.__generate_hash(data.get("password"))
        self.created_at = datetime.datetime.utcnow()
        self.updated_at = datetime.datetime.utcnow()

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()

    def update(self, data) -> None:
        for key, item in data.items():
            if key == "password":
                self.password = self.__generate_hash(item)
            setattr(self, key, item)
        self.updated_at = datetime.datetime.utcnow()
        db.session.commit()

    def delete(self) -> None:
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all_users():
        return User.query.all()

    @staticmethod
    def get_one_user(id_: str):
        return User.query.get(id_)

    @staticmethod
    def get_user_by_email(email_: str):
        return User.query.filter_by(email=email_).first()

    def __repr(self):
        return "<id {}>".format(self.id)

    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password=password, rounds=10).decode(
            "utf-8"
        )

    def check_hash(self, password):
        return bcrypt.check_password_hash(pw_hash=self.password, password=password)


class UserSchema(Schema):
    """
    User Schema
    """

    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
