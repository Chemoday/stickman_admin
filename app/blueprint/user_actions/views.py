from flask import render_template, url_for,request, abort, jsonify

from . import user_actions
from ..auth_http import auth_api_handler
from ..profile_actions import profile_actions
from playhouse.shortcuts import model_to_dict
from app.models.models import Users, UserProfiles,UserProfileWeapons, BalanceHistory, UserStats
from app.utils.validators import validate_int_json_data, validate_string_json_data
from app import db


@user_actions.route('/admin/user/get-all', methods=['POST'])
@auth_api_handler.login_required
def user_get_all_info():
    user_id = validate_int_json_data(argument_name='user_id')
    if Users.select().where(Users.id == user_id).exists():
        user = Users.get(Users.id == user_id)
    else:
        return jsonify({
            'result': 'ERROR',
            'reason': 'User with this user_id is not exist'
        })
    #TODO All info
    user_stats = UserStats.get_user_stats(user_id=user_id)
    profiles = UserProfiles.get_profile(user_id=user_id)
    balance_history = BalanceHistory.get_account_balance_history(id=user_id, search_by='user')
    data = {
        'user': model_to_dict(user, exclude=[Users.password, Users.settings],),
        'user_stats': model_to_dict(user_stats),
        'profiles': profiles,
        'balance_history': balance_history
    }

    return jsonify({
        'user_data': data,
        'result': 'OK'})




@user_actions.route('/admin/user/stats', methods=['POST'])
@auth_api_handler.login_required
def user_get_stats():
    user_id = validate_int_json_data(argument_name='user_id')
    stats = UserStats.get_user_stats(user_id=user_id)
    if stats:
        return jsonify({'result': 'OK',
                        'user_stats': model_to_dict(stats)})
    else:
        return jsonify({'result': 'ERROR',
                        'reason': 'User is not exist or have no stats registered'})



@user_actions.route('/admin/user/search/by-numeric-data', methods = ['POST'])
@auth_api_handler.login_required
def player_entity_search():
    users_data = {}
    entity_id = validate_int_json_data(argument_name='entity_id')

    q = Users.select().where( (Users.id == entity_id) | (Users.account == entity_id))
    if q.exists():
        users = q
        for user in users:
            users_data[str(user.id)] = model_to_dict(user, exclude=[Users.password,
                                                          Users.settings])
    else:
        return jsonify({'reason': 'User is not exist',
                        'result': 'ERROR'})

    profiles_data = profile_actions._get_profile(profile_id=entity_id)
    entity_data = {'users': users_data,
                   'profile': model_to_dict(profiles_data, exclude=[UserProfiles.vip_end_dt])}



    return jsonify({'result': 'OK',
                    'entity_id':entity_data})

@auth_api_handler.login_required
@user_actions.route('/admin/user/update/nickname', methods=['POST'])
def update_user_nickname():
    user_id = validate_int_json_data(argument_name='user_id')
    new_nickname = validate_string_json_data(argument_name='new_nickname')
    updated_row = Users.update(nickname=new_nickname).where(Users.id == user_id).execute()
    if updated_row > 0:
        return jsonify({'result': 'OK'})
    else:
        return jsonify({'result': 'ERROR',
                        'reason': 'nickname was not updated, something went wrong'})



@auth_api_handler.login_required
@user_actions.route('/admin/user/payments', methods=['POST'])
def get_user_payments():
    platform = 'android'

    user_id = validate_int_json_data(argument_name='user_id')
    if request.method == 'POST':

        platform = validate_string_json_data(argument_name='platform')

    #TODO add handlers
    data = BalanceHistory.get_payments_history(user_id=user_id, platform=platform)
    return jsonify({
        'result': 'OK',
        'data': data
    })
