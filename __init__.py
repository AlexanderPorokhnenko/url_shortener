import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow
from .config import config_by_name


db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()


def create_app(config_name):
    app = Flask(__name__)
    config_name = os.environ.get('FLASK_CONFIG', config_name)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    from .api import api, api_bp
    api.init_app(app)
    app.register_blueprint(api_bp)
    with app.app_context():
        db.create_all()
    return app
