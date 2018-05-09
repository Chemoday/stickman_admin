import os
from app import create_app


from flask_script import Manager, Shell

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)


@manager.command
def generate_db_tables():
    from app import db
    from app.models.models import MODELS_LIST
    from config import DevelopmentConfig
    db.initialize(DevelopmentConfig.DATABASE)
    for model in MODELS_LIST:
        db.create_table(model, safe=True)
    print("Db tables created")


if __name__ == '__main__':
    manager.run()

