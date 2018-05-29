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


@main_bp.route('/test', )
def test():
    cursor = db.execute_sql('select find_top_total_kills()')
    for row in cursor.fetchall():
        print(row, type(row[0]))
    return jsonify({})