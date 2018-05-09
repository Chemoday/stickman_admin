from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from peewee import *

from app import db
from app.utils.auth import token_generator


class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = PrimaryKeyField()
    username = CharField(max_length=20)
    password_hash = CharField(max_length=128)




    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)

    @property
    def password(self):
        raise AttributeError or('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self):
        return token_generator.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        try:
            data = token_generator.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.get(User.id == data['id'])
        return user

    class Meta:
        db_table = 'users'

MODELS_LIST = [User]