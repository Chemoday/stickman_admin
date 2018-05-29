from flask import render_template, url_for,request, abort, jsonify

from . import statistics
from ..auth_http import auth_api_handler
from playhouse.shortcuts import model_to_dict
from app.models.models import Users, UserProfiles,UserProfileWeapons, BalanceHistory, UserStats
from app.utils.validators import validate_int_json_data
from app import db