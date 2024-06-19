# apps/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mghgou%40%23%24%25%5E87%29%28%2A%2A%29@localhost/holochron_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
   
    from apps.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
