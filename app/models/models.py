from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from peewee import *
import datetime
from .. import db
from app.utils.auth import token_generator

# database = PostgresqlDatabase('stickman', **{'user': 'postgres', 'port': 5444})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = db

class Admins(BaseModel):
    last_login_dt = DateTimeField(null=True)
    moderator = BooleanField(constraints=[SQL("DEFAULT false")])
    password = CharField(null=True)
    token = CharField(null=True)
    token_created_dt = DateTimeField(null=True)
    username = CharField(null=True)
    id = PrimaryKeyField()

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    @property
    def password_hash(self):
        raise AttributeError or('password is not a readable attribute')

    @password_hash.setter
    def password_hash(self, password):
        self.password = generate_password_hash(password)
        print(self.password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self):
        return token_generator.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        try:
            data = token_generator.loads(token)
        except SignatureExpired:
            return None, SignatureExpired  # valid token, but expired
        except BadSignature:
            return None, None  # invalid token
        admin = Admins.get(Admins.id == data['id'])
        return admin, None

    class Meta:
        table_name = 'admins'

class AdminHistory(BaseModel):
    action = IntegerField(null=True)
    admin = IntegerField(column_name='admin_id', null=True)
    created_dt = TimeField(null=True)

    class Meta:
        table_name = 'admin_history'
        schema = 'public'
        primary_key = False


class Users(BaseModel):
    account = CharField(column_name='account_id')
    active = BooleanField(constraints=[SQL("DEFAULT false")], null=True)
    active_days = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ban = BooleanField(constraints=[SQL("DEFAULT false")])
    ban_end_dt = DateTimeField(null=True)
    ban_reason = CharField(null=True)
    created_dt = DateTimeField(constraints=[SQL("DEFAULT now()")], null=True)
    gold = IntegerField(constraints=[SQL("DEFAULT 10")])
    gold_contests_unlocked = BooleanField(constraints=[SQL("DEFAULT false")])
    last_login_dt = DateTimeField(null=True)
    moderator = BooleanField(constraints=[SQL("DEFAULT false")], null=True)
    network = IntegerField(column_name='network_id', constraints=[SQL("DEFAULT 0")])
    nickname = CharField()
    nickname_changed = BooleanField(constraints=[SQL("DEFAULT false")])
    password = CharField()
    play_time_left = IntegerField(constraints=[SQL("DEFAULT 43200")])
    reference = IntegerField(null=True)
    settings = TextField(null=True)
    shards = IntegerField(constraints=[SQL("DEFAULT 0")])
    silver = IntegerField(constraints=[SQL("DEFAULT 800")])
    total_play_time = IntegerField(constraints=[SQL("DEFAULT 0")])
    updated_dt = DateTimeField(null=True)
    verified_dt = DateTimeField(null=True)
    zone = IntegerField(column_name='zone_id', null=True)

    class Meta:
        table_name = 'users'


