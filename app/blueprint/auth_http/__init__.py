from flask import Blueprint
from flask_httpauth import HTTPBasicAuth

auth_api = Blueprint('auth_http', __name__)
auth_api_handler = HTTPBasicAuth()

from . import views


