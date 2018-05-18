from flask import render_template, url_for,request, abort, jsonify

from . import main_bp
from ..auth_http import auth_api_handler
from .forms import NameForm
from playhouse.shortcuts import model_to_dict
from app.models.models import Users, UserProfiles,UserProfileWeapons
from app import db

@main_bp.route('/', methods=['GET', 'POST'])
@auth_api_handler.login_required
def index():
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

@main_bp.route('/test')
@auth_api_handler.login_required
def test():
    print('here')
    cursor = db.execute_sql('SELECT public.find_top_total_kills();')
    for row in cursor.fetchall():
        print(row[0])
    return jsonify({})



@main_bp.route('/admin/profile/all-info', methods = ['POST'])
@auth_api_handler.login_required
def profile_get_all_info():
    try:
        profile_id = request.json.get('id')
    except Exception as e:
        print(e)
        return jsonify({'error': 'wrong argument, awaiting <id>'})
    if type(profile_id) != int:
        return jsonify({"error": 'wrong data type'})

    if UserProfiles.select().where(UserProfiles.id == profile_id).exists():
        profile = UserProfiles.get(UserProfiles.id == profile_id)
    else:
        return jsonify({'error': 'profile with this id is not exists'})

    weapons = _get_profile_weapons(profile_id)

    data = {'profile': model_to_dict(profile, exclude=[UserProfiles.vip_end_dt]),
            'weapons': weapons}

    return jsonify(data)

def _get_profile_weapons(profile_id):
    weapons = {}
    profile_weapons = UserProfileWeapons.select().where(UserProfileWeapons.user_profile == profile_id)
    for id, weapon in enumerate(profile_weapons):
        weapons[str(id)] = model_to_dict(weapon)
    return weapons