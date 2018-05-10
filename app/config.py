import os
import peewee
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'

    POSTS_PER_PAGE = 10
    TOKEN_LIFETIME = 600

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True

    host= 'localhost'
    port= 5444
    user= 'postgres'
    password = 'postgres'
    DATABASE = peewee.PostgresqlDatabase('stickman', user=user, password=password,
                                         host=host, port=port)


class TestingConfig(Config):
    DEBUG = False
    DATABASE = {
        'name': 'test.db',
        'engine': 'peewee.SqliteDatabase'
    }

class ProductionConfig(Config):
    pass

config_select = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}