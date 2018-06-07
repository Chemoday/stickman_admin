from flask import render_template, url_for,request, abort, jsonify
from peewee import fn
from . import statistics
from ..auth_http import auth_api_handler
from playhouse.shortcuts import model_to_dict
from app.models.models import *
from app.utils.validators import validate_int_json_data
from app import db

from collections import OrderedDict

@statistics.route('/admin/stat/popular-weapons')
@auth_api_handler.login_required
def get_popular_weapons():
    popular_weapons = Weapons.\
        select(UserProfileWeapons.weapon, Weapons.name, fn.COUNT(UserProfileWeapons.id))\
        .join(UserProfileWeapons, on=(Weapons.id == UserProfileWeapons.weapon))\
        .where(UserProfileWeapons.equipped == True)\
        .group_by(Weapons.name, UserProfileWeapons.weapon)\
        .order_by(fn.COUNT(UserProfileWeapons.id).desc())


    weapons = {}
    for weapon in popular_weapons:
        weapons[weapon.name] = weapon.count

    return jsonify({
        'result': 'OK',
        'weapons': weapons
    })


@statistics.route('/admin/stat/popular-armors')
@auth_api_handler.login_required
def get_popular_armors():
    popular_armors = Armors.\
        select(UserProfileArmors.armor, Armors.name, fn.COUNT(UserProfileArmors.armor))\
        .join(UserProfileArmors, on=(Armors.id == UserProfileArmors.armor))\
        .group_by(Armors.name, UserProfileArmors.armor)\
        .order_by(fn.COUNT(UserProfileArmors.armor).desc())

    armors = {}
    print(len(popular_armors))
    for armor in popular_armors:
        armors[armor.name] = armor.count

    return jsonify({
        'result': 'OK',
        'armors': armors
    })


@statistics.route('/admin/stat/richest-users')
@auth_api_handler.login_required
def get_richest_users():
    query = Users.select(Users.nickname, Users.silver).order_by((Users.silver).desc()).limit(5)
    users = OrderedDict()
    for user in query:
        print(user.nickname, user.silver)
        users[user.nickname] = user.silver

    return jsonify({
        'result': 'OK',
        'users': users
    })



