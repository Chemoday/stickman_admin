from flask import render_template, url_for,request, abort, jsonify

from . import profile_actions
from ..auth_http import auth_api_handler


from playhouse.shortcuts import model_to_dict
from app.models.models import Users, UserProfiles,UserProfileWeapons, BalanceHistory, UserStats
from app.utils.validators import validate_int_json_data



@profile_actions.route('/admin/profile/get-all', methods=['POST'])
@auth_api_handler.login_required
def profile_get_all_info(profile_id=None):

    profile_id = validate_int_json_data(argument_name='profile_id')
    profile = UserProfiles.get_profile(profile_id=profile_id)

    if not profile:
        return jsonify({'result': 'ERROR',
                        'reason': 'profile with this id is not exists'})

    weapons = UserProfileWeapons.get_profile_weapons(profile_id)
    balance_history = BalanceHistory.get_account_balance_history(search_by='profile', id=profile_id)
    data = {'profile': model_to_dict(profile, exclude=[UserProfiles.vip_end_dt]),
            'weapons': weapons,
            'balance_history': balance_history
            }

    return jsonify({'result': 'OK',
                    'profile_data': data})

@profile_actions.route('/admin/profile/get', methods=['POST'])
@auth_api_handler.login_required
def profile_get(profile_id=None):
    if not profile_id:
        profile_id = validate_int_json_data(argument_name='profile_id')

    profile = UserProfiles.get_profile(profile_id=profile_id)

    if not profile:
        return jsonify({'result': 'ERROR',
                        'reason': 'profile with this id is not exists'})
    return jsonify(model_to_dict(profile, exclude=[UserProfiles.vip_end_dt]))


