from flask import render_template, url_for,request, abort, jsonify

from . import profile_actions
from ..auth_http import auth_api_handler
from ..user_actions import user_actions
from playhouse.shortcuts import model_to_dict
from app.models.models import Users, UserProfiles,UserProfileWeapons, BalanceHistory, UserStats
from app.utils.validators import validate_int_json_data
from app import db


@profile_actions.route('/admin/profile/get-all', methods=['POST'])
@auth_api_handler.login_required
def profile_get_all_info(profile_id=None):
    if not profile_id:
        profile_id = validate_int_json_data(argument_name='profile_id')

    profile = _get_profile(profile_id=profile_id)

    if not profile:
        return jsonify({'result': 'ERROR',
                        'reason': 'profile with this id is not exists'})

    weapons = _get_profile_weapons(profile_id)
    balance_history = user_actions._get_account_balance_history(search_by='profile', id=profile_id)
    data = {'profile': model_to_dict(profile, exclude=[UserProfiles.vip_end_dt]),
            'weapons': weapons,
            'balance_history': balance_history,
            'result': 'OK'}

    return jsonify({'reason': 'OK',
                    'profile': data})

@profile_actions.route('/admin/profile/get', methods=['POST'])
@auth_api_handler.login_required
def profile_get(profile_id=None):
    if not profile_id:
        profile_id = validate_int_json_data(argument_name='profile_id')

    profile = _get_profile(profile_id=profile_id)

    if not profile:
        return jsonify({'result': 'ERROR',
                        'reason': 'profile with this id is not exists'})
    return jsonify(model_to_dict(profile, exclude=[UserProfiles.vip_end_dt]))


#database hooks
def _get_profile(profile_id):
     if UserProfiles.select().where(UserProfiles.id == profile_id).exists():
        profile = UserProfiles.get(UserProfiles.id == profile_id)
        return profile
     else:
        return

def _get_profile_weapons(profile_id):
    weapons = {}
    profile_weapons = UserProfileWeapons.select().where(UserProfileWeapons.user_profile == profile_id)
    for id, row in enumerate(profile_weapons):
        weapons[str(row.weapon)] = model_to_dict(row)
    return weapons

