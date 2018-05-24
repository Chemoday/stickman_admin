from flask import render_template, url_for,request, abort, jsonify

from . import main_bp
from ..auth_http import auth_api_handler
from .forms import NameForm
from playhouse.shortcuts import model_to_dict
from app.models.models import Users, UserProfiles,UserProfileWeapons, BalanceHistory, UserStats
from app.utils.validators import validate_int_json_data
from app import db

@main_bp.route('/', methods=['GET', 'POST'])
@auth_api_handler.login_required
def index():
    #Just to test, will be removed.
    form = NameForm()
    if form.validate_on_submit():
        q = Users.select().where(Users.id == form.name.data)
        if q.exists():
            user = Users.select().where(Users.id == form.name.data).first()
            print(user.id, user.nickname)
            return render_template('index.html', user=user, form=form)
        else:
            return url_for('.index', form=form)
    return render_template('index.html', form=form)


@main_bp.route('/admin/profile/get-all', methods=['POST'])
@auth_api_handler.login_required
def profile_get_all_info(profile_id=None):
    if not profile_id:
        profile_id = validate_int_json_data(argument_name='profile_id')

    profile = _get_profile(profile_id=profile_id)

    if not profile:
        return jsonify({'error': 'profile with this id is not exists'})

    weapons = _get_profile_weapons(profile_id)
    balance_history = _get_account_balance_history(search_by='profile', id=profile_id)
    data = {'profile': model_to_dict(profile, exclude=[UserProfiles.vip_end_dt]),
            'weapons': weapons,
            'balance_history': balance_history}
    return jsonify(data)

@main_bp.route('/admin/profile/get', methods=['POST'])
@auth_api_handler.login_required
def profile_get(profile_id=None):
    if not profile_id:
        profile_id = validate_int_json_data(argument_name='profile_id')

    profile = _get_profile(profile_id=profile_id)

    if not profile:
        return jsonify({'error': 'profile with this id is not exists'})
    return jsonify(model_to_dict(profile, exclude=[UserProfiles.vip_end_dt]))


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



@main_bp.route('/admin/user/stats', methods = ['POST'])
@auth_api_handler.login_required
def user_get_stats():
    user_id = validate_int_json_data(argument_name='user_id')
    q = UserStats.select().where(UserStats.user == user_id)
    if q.exists():
        stats = UserStats.get(UserStats.user == user_id)
        return jsonify(model_to_dict(stats))
    else:
        return jsonify({'error': 'User is not exist'})



@main_bp.route('/admin/user/search/by-numeric-data', methods = ['POST'])
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

    profiles_data = _get_profile(profile_id=entity_id)
    entity_data = {'users': users_data,
                   'profile': model_to_dict(profiles_data, exclude=[UserProfiles.vip_end_dt])}



    return jsonify(entity_data)



@main_bp.route('/test')
def test():
    cursor = db.execute_sql('select find_top_total_kills()')
    for row in cursor.fetchall():
        print(row, type(row[0]))
