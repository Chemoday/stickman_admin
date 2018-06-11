from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)
from peewee import *
from playhouse.shortcuts import model_to_dict
import datetime
from .. import db
from app.utils.auth import token_generator

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
    created_dt = DateTimeField(null=True, default=datetime.datetime.now())
    username = CharField(null=True)

    class Meta:
        table_name = 'admin_history'



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


class UserProfiles(BaseModel):
    character = IntegerField(column_name='character_id')
    exp = IntegerField(constraints=[SQL("DEFAULT 0")])
    last_level_up_dt = DateTimeField(null=True)
    level = IntegerField(constraints=[SQL("DEFAULT 0")])
    mod = IntegerField()
    next_level_exp = IntegerField(constraints=[SQL("DEFAULT 150")])
    profile = IntegerField(column_name='profile_id')
    rating = IntegerField(constraints=[SQL("DEFAULT 0")])
    selected = BooleanField(constraints=[SQL("DEFAULT true")])
    skill_points = IntegerField(constraints=[SQL("DEFAULT 0")])
    total_deaths = IntegerField(constraints=[SQL("DEFAULT 0")])
    total_frags = IntegerField(constraints=[SQL("DEFAULT 0")])
    total_wins = IntegerField(constraints=[SQL("DEFAULT 0")])
    user = IntegerField(column_name='user_id', index=True)
    vip_end_dt = DateTimeField(null=True)
    weapons_slots = IntegerField(constraints=[SQL("DEFAULT 3")])

    class Meta:
        table_name = 'user_profiles'


    @staticmethod
    def get_profile(profile_id=-1, user_id=None):
        if user_id:
            if UserProfiles.select().where(UserProfiles.user == user_id).exists():
                profiles = {}
                profiles_query = UserProfiles.select().where(UserProfiles.user == user_id)

                for profile in profiles_query:
                    profiles[profile.id] = model_to_dict(profile)

                return profiles

            else:
                return

        if UserProfiles.select().where(UserProfiles.id == profile_id).exists():
            profile = UserProfiles.get(UserProfiles.id == profile_id)
            return profile
        else:
            return


class UserProfileWeapons(BaseModel):
    equipped = BooleanField(constraints=[SQL("DEFAULT false")], null=True)
    extra_ammo_level = IntegerField(constraints=[SQL("DEFAULT 0")])
    extra_damage_level = IntegerField(constraints=[SQL("DEFAULT 0")])
    extra_recoil_level = IntegerField(constraints=[SQL("DEFAULT 0")])
    extra_reload_level = IntegerField(constraints=[SQL("DEFAULT 0")])
    extra_shot_interval_level = IntegerField(constraints=[SQL("DEFAULT 0")])
    extra_spread_level = IntegerField(constraints=[SQL("DEFAULT 0")])
    headshots = IntegerField(constraints=[SQL("DEFAULT 0")])
    kills = IntegerField(constraints=[SQL("DEFAULT 0")])
    level = IntegerField(constraints=[SQL("DEFAULT 0")])
    rent_end_dt = DateTimeField(null=True)
    rent_forever = BooleanField(constraints=[SQL("DEFAULT false")], null=True)
    selected = BooleanField(constraints=[SQL("DEFAULT false")], null=True)
    teammate_kills = IntegerField(constraints=[SQL("DEFAULT 0")])
    unlocked_dt = DateTimeField(null=True)
    upgrade_points = IntegerField(constraints=[SQL("DEFAULT 0")])
    user_profile = IntegerField(column_name='user_profile_id', index=True)
    victory_kills = IntegerField(constraints=[SQL("DEFAULT 0")])
    weapon = IntegerField(column_name='weapon_id')

    class Meta:
        table_name = 'user_profile_weapons'

    @staticmethod
    def get_profile_weapons(profile_id):
        weapons = {}
        profile_weapons = UserProfileWeapons.select().where(UserProfileWeapons.user_profile == profile_id)
        for id, row in enumerate(profile_weapons):
            weapons[str(row.weapon)] = model_to_dict(row)
        return weapons

class UserProfileArmors(BaseModel):
    armor = IntegerField(column_name='armor_id')
    created_dt = DateTimeField(constraints=[SQL("DEFAULT now()")], null=True)
    current_durability = IntegerField()
    equipped = BooleanField(constraints=[SQL("DEFAULT false")], null=True)
    user_profile = IntegerField(column_name='user_profile_id')

    class Meta:
        table_name = 'user_profile_armors'
        indexes = (
            (('user_profile', 'armor'), True),
        )
        primary_key = CompositeKey('armor', 'user_profile')


class UserProfileSkills(BaseModel):
    accuracy = IntegerField(constraints=[SQL("DEFAULT 0")])
    defence = IntegerField(constraints=[SQL("DEFAULT 0")])
    explosions = IntegerField(constraints=[SQL("DEFAULT 0")])
    health = IntegerField(constraints=[SQL("DEFAULT 0")])
    luck = IntegerField(constraints=[SQL("DEFAULT 0")])
    strength = IntegerField(constraints=[SQL("DEFAULT 0")])
    user_profile = IntegerField(column_name='user_profile_id')

    class Meta:
        table_name = 'user_profile_skills'

class UserRatings(BaseModel):
    daily_rating = IntegerField(constraints=[SQL("DEFAULT 0")])
    global_rating = IntegerField(constraints=[SQL("DEFAULT 1000")])
    monthly_rating = IntegerField(constraints=[SQL("DEFAULT 0")])
    season_rating = IntegerField(constraints=[SQL("DEFAULT 0")])
    user = AutoField(column_name='user_id')
    weekly_rating = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'user_ratings'

class UserStats(BaseModel):
    achievement_points = IntegerField(constraints=[SQL("DEFAULT 0")])
    ctf_wins = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivered_flags = IntegerField(constraints=[SQL("DEFAULT 0")])
    dm_wins = IntegerField(constraints=[SQL("DEFAULT 0")])
    dom_wins = IntegerField(constraints=[SQL("DEFAULT 0")])
    double_kills = IntegerField(constraints=[SQL("DEFAULT 0")])
    elm_wins = IntegerField(constraints=[SQL("DEFAULT 0")])
    headshots = IntegerField(constraints=[SQL("DEFAULT 0")])
    melee_kills = IntegerField(constraints=[SQL("DEFAULT 0")])
    multi_kills = IntegerField(constraints=[SQL("DEFAULT 0")])
    mvp = IntegerField(constraints=[SQL("DEFAULT 0")])
    play_time = IntegerField(constraints=[SQL("DEFAULT 0")])
    tdm_wins = IntegerField(constraints=[SQL("DEFAULT 0")])
    total_deaths = IntegerField(constraints=[SQL("DEFAULT 0")])
    total_kills = IntegerField(constraints=[SQL("DEFAULT 0")])
    user = AutoField(column_name='user_id')

    class Meta:
        table_name = 'user_stats'
        schema = 'public'

    @staticmethod
    def get_user_stats(user_id):
        if UserStats.select().where(UserStats.user == user_id).exists():
            stats = UserStats.get(UserStats.user == user_id)
            return stats
        else:
            return

class BalanceHistory(BaseModel):
    comment = CharField(null=True)
    created_dt = DateTimeField(constraints=[SQL("DEFAULT now()")])
    gold = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods = IntegerField(column_name='goods_id', constraints=[SQL("DEFAULT 0")])
    goods_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    shards = IntegerField(constraints=[SQL("DEFAULT 0")])
    silver = IntegerField(constraints=[SQL("DEFAULT 0")])
    source = IntegerField(constraints=[SQL("DEFAULT 0")])
    user = ForeignKeyField(column_name='user_id', field='id', model=Users)
    user_profile = IntegerField(column_name='user_profile_id')

    class Meta:
        table_name = 'balance_history'
        schema = 'public'

    @staticmethod
    def get_account_balance_history(id, search_by='user'):
        """

        :param id: profile_id or user_id of player
        :param search_by: accepts only string - user or profile
        :return: player balance history depends of search type
        """
        #TODO make universal function, search by various parameters

        balance_history = {}
        if search_by == 'user':
            history = BalanceHistory.select().where(BalanceHistory.user == id)
        elif search_by =='profile':
            history = BalanceHistory.select().where(BalanceHistory.user_profile == id)
        else:
            return False


        for row in history:
            balance_history[str(row.id)] = model_to_dict(row, max_depth=0)

        return balance_history

class Weapons(BaseModel):
    ammo = IntegerField()
    attack_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    bullets = IntegerField()
    bullets_per_reload = IntegerField()
    business_data = TextField(constraints=[SQL("DEFAULT '{}'::text")])
    capacity = IntegerField()
    category = IntegerField(column_name='category_id')
    damage = IntegerField()
    enabled = BooleanField(constraints=[SQL("DEFAULT true")])
    jackpot = BooleanField(constraints=[SQL("DEFAULT false")])
    list_index = IntegerField()
    min_accuracy = IntegerField(constraints=[SQL("DEFAULT 0")])
    min_explosions = IntegerField(constraints=[SQL("DEFAULT 0")])
    min_strength = IntegerField(constraints=[SQL("DEFAULT 0")])
    name = CharField(null=True)
    recoil = IntegerField()
    reload_time = IntegerField()
    sell_allowed = BooleanField(constraints=[SQL("DEFAULT true")], null=True)
    shot_interval = IntegerField()
    spread = IntegerField()
    start_level = IntegerField(constraints=[SQL("DEFAULT 0")])
    weight = DecimalField(constraints=[SQL("DEFAULT 0.0")])

    class Meta:
        table_name = 'weapons'
        schema = 'public'


class Armors(BaseModel):
    armor_points = IntegerField()
    business_data = TextField(constraints=[SQL("DEFAULT '{}'::text")])
    durability = IntegerField()
    durability_type = CharField()
    enabled = BooleanField(constraints=[SQL("DEFAULT true")], null=True)
    energy_defense = FloatField()
    explosion_defense = FloatField()
    heavy_defense = FloatField()
    medium_defense = FloatField()
    min_level = IntegerField()
    name = CharField(null=True)
    small_defense = FloatField()

    class Meta:
        table_name = 'armors'
        schema = 'public'

