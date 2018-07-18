from flask import render_template, url_for,request, abort, jsonify
from peewee import fn
from . import statistics
from ..auth_http import auth_api_handler
from playhouse.shortcuts import model_to_dict
from app.models.models import *
from app.models.statistics.models import GameRounds
from app.utils.validators import validate_int_json_data
from app import db

import datetime
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


@statistics.route('/admin/stat/richest-users', methods=['GET', 'POST'])
@auth_api_handler.login_required
def get_richest_users():
    amount = 15
    if request.method == 'POST':
        amount = validate_int_json_data(argument_name='amount')

    query = Users.select(Users.nickname, Users.silver).order_by((Users.silver).desc()).limit(amount)
    users = OrderedDict()
    for user in query:
        users[user.nickname] = user.silver

    return jsonify({
        'result': 'OK',
        'users': users
    })


@statistics.route('/admin/stat/week-money-gain', methods=['GET', 'POST'])
@auth_api_handler.login_required
def weekly_money_gain():
    days_to_substract = 7
    if request.method == 'POST':
        days_to_substract = validate_int_json_data(argument_name='days')

    current_date = datetime.datetime.now()
    date_range = current_date - datetime.timedelta(days=days_to_substract)

    query = Users\
        .select(Users.id, Users.nickname,
                fn.SUM(BalanceHistory.silver).alias('sum_silver'), fn.SUM(BalanceHistory.gold).alias('sum_gold'))\
        .join(BalanceHistory, on=(Users.id == BalanceHistory.user))\
        .where((BalanceHistory.created_dt > date_range))\
        .group_by(Users.id, Users.nickname)\
        .order_by(fn.SUM(BalanceHistory.gold).desc())
    data = {}


    for row in query:
        data[row.nickname] = {}
        data[row.nickname]['silver'] = row.sum_silver
        data[row.nickname]['gold'] = row.sum_gold


        #Return {'nickname' : {'gold': 0, 'silver': 0}}
    return jsonify({
        'result': 'OK',
        'data': data
    })

