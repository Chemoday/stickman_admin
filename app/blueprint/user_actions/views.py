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

    data = {
        'user': model_to_dict(user)
    }

    return jsonify({
        'data': data,
        'result': 'OK'})




@user_actions.route('/admin/user/stats', methods=['POST'])
@auth_api_handler.login_required
def user_get_stats():
    user_id = validate_int_json_data(argument_name='user_id')
    q = UserStats.select().where(UserStats.user == user_id)
    if q.exists():
        stats = UserStats.get(UserStats.user == user_id)
        return jsonify({'stats': model_to_dict(stats),
                        'result': 'OK'})
    else:
        return jsonify({'reason': 'User is not exist',
                        'result': 'ERROR'})



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
    print('User_ID:{0} | nickname: {1}'.format(user_id, new_nickname))
    # q = Users.select().where(Users.nickname == new_nickname)
    updated_row = Users.update(nickname=new_nickname).where(Users.id == user_id).execute()
    if updated_row > 0:
        return jsonify({'result': 'OK'})
    else:
        return jsonify({'result': 'ERROR',
                        'reason': 'nickname was not updated, something went wrong'})




#database hooks
def _get_account_balance_history(id, search_by='user'):
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
        balance_history[row.id] = model_to_dict(row, max_depth=0)

    return balance_history

