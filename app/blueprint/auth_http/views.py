from flask import request, abort, jsonify, url_for, g

from . import auth_api, auth_api_handler

from flask import  Response
from playhouse.shortcuts import model_to_dict

from app.models.models import User

@auth_api.route('/auth_http/register', methods = ['POST'])
def create_user():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
    except:
        abort(406)

    if username is None or password is None:
        abort(400) # missing arguments
    if User.select().where(User.username == username).exists():
        return Response("{'error':'User with this data is exists'}", status=416, mimetype='application/json')
    if len(username) < 5 or len(password) < 5:
        return Response("{'error':'Login or password is too short'}", status=415, mimetype='application/json')

    user = User.create(username=username,
                       password=password)
    res=jsonify({'username': user.username})

    return res



@auth_api.route('/auth_http/request-token')
@auth_api_handler.login_required
def request_token():
    token = g.user.generate_auth_token()
    return jsonify({'token': token.decode('ascii'),
                    'username': g.user.username})


@auth_api_handler.verify_password
def verify_password(username_or_token, password):
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.select().where(User.username==username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True

@auth_api.route('/user',  methods = ['POST'])
@auth_api_handler.login_required
def request_user():
    user = g.user
    return jsonify(model_to_dict(user, exclude=[User.password_hash]))