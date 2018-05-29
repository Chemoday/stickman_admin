from flask import Blueprint

profile_actions = Blueprint('profile_actions', __name__)


from . import views