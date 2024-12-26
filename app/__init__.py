import sqlite3
from flask import Flask, g
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from . import routes
    app.register_blueprint(routes.app)

    @app.before_request
    def connect_db():
        g.db = sqlite3.connect(app.config['DATABASE_PATH'])

    @app.teardown_request
    def close_db(exception):
        db = getattr(g, 'db', None)
        if db is not None:
            db.close()

    return app
