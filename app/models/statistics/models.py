from peewee import *
import datetime
from ... import db




class BaseModel(Model):
    class Meta:
        database = db
        schema = 'stat'



class GameRounds(BaseModel):
    #TODO ask Kostja about map format
    mode = CharField(index=True, max_length=20)
    type = CharField(index=True, max_length=20)
    map = CharField(index=True, max_length=20)
    total_players = IntegerField()
    total_kills = IntegerField()
    total_deaths = IntegerField()
    most_kills = IntegerField()
    most_deaths = IntegerField()
    created_dt = DateTimeField(default=datetime.datetime.now())


MODELS_LIST = [GameRounds]