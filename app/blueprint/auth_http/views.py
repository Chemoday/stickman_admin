from flask import request, abort, jsonify, url_for, g
from . import auth_api, auth_api_handler
from flask import  Response
from playhouse.shortcuts import model_to_dict
from itsdangerous import BadTimeSignature, BadSignature

import datetime



from app.models.models import Admins, Users

@auth_api.route('/admin/register', methods = ['POST'])
def register_admin():
    registration_open = True
    if not registration_open:
        abort(401)
    else:
        try:
            username = request.json.get('username')
            password = request.json.get('password')
        except:
            abort(406)

        if username is None or password is None:
            abort(400) # missing arguments
        if Admins.select().where(Admins.username == username).exists():
            return Response("{'error':'User with this data is exists'}", status=416, mimetype='application/json')
        if len(username) < 5 or len(password) < 5:
            return Response("{'error':'Login or password is too short'}", status=415, mimetype='application/json')
        admin = Admins.create(username=username, password_hash=password)
        token = admin.generate_auth_token()
        admin.token = token
        admin.save(only=[Admins.token])
        res = jsonify({'username': admin.username,
                     'token': admin.token.decode('ascii')})

        return res

@auth_api.route('/admin/login')
@auth_api_handler.login_required
def login():
    pass


@auth_api.route('/admin/request-token')
@auth_api_handler.login_required
def request_token():
    if not g.admin.token or not g.good_token_state:
        token = g.admin.generate_auth_token()
        g.admin.token = token
        g.admin.save(only=[Admins.token])
        return jsonify({'token': token.decode('ascii'),
                    'username': g.admin.username,
                        'new': True})
    else:
        token = g.admin.token
        return jsonify({'token': token,
                        'username': g.admin.username,
                       'new': False})


@auth_api_handler.verify_password
def verify_password(username_or_token, password):
    admin, token_state = Admins.verify_auth_token(username_or_token)
    if token_state == BadTimeSignature:
        return abort(403)
    if not admin:
        # try to authenticate with username/password
        admin = Admins.select().where(Admins.username==username_or_token).first()
        if not admin or not admin.verify_password(password):
            return False
    g.admin = admin
    g.good_token_state = True
    return True

@auth_api.route('/admin',  methods = ['POST'])
@auth_api_handler.login_required
def request_user():
    admin = g.admin
    return jsonify(model_to_dict(admin, exclude=[Admins.password]))

