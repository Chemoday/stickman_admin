from flask import Flask
from flask_peewee.db import Proxy, Database
from flask_bootstrap import Bootstrap

from app.config import config_select

db = Proxy()
bootstrap = Bootstrap()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_select[config_name])
    db.initialize(config_select[config_name].DATABASE)
    bootstrap.init_app(app)

    #register blueprints
    from app.blueprint.main import main_bp as main_blueprint
    app.register_blueprint(main_blueprint)

    from app.blueprint.auth_http import auth_api
    app.register_blueprint(auth_api)

    from app.blueprint.user_actions import user_actions
    app.register_blueprint(user_actions)

    from app.blueprint.profile_actions import profile_actions
    app.register_blueprint(profile_actions)

    from app.blueprint.statistics import statistics
    app.register_blueprint(statistics)

    return app
