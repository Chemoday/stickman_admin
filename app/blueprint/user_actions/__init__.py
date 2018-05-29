from flask import Blueprint

user_actions = Blueprint('user_actions', __name__)


from . import views