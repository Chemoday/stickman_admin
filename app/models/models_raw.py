from peewee import *

database = PostgresqlDatabase('stickman', **{'user': 'postgres', 'port': 5444})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class Admins(BaseModel):
    last_login_dt = DateTimeField(null=True)
    moderator = BooleanField(constraints=[SQL("DEFAULT false")])
    password = CharField(null=True)
    token = CharField(null=True)
    token_created_dt = DateTimeField(null=True)
    username = CharField(null=True)

    class Meta:
        table_name = 'admins'

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


