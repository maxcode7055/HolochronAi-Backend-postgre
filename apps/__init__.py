# apps/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from .flask_mail_config import mail
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
import os

load_dotenv()
db = SQLAlchemy()
def create_app():
    app = Flask(__name__, static_folder='uploads')
    jwt = JWTManager(app)
    CORS(app)
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') 
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')  # or 465 for SSL
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')  # Set to False if using SSL
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['DEVELOPMENT_FRONT_URL'] = os.getenv('DEVELOPMENT_FRONT_URL')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:Mghgou%40%23%24%25%5E87%29%28%2A%2A%29@localhost/holochron_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = os.getenv('OPEN_AI_SECRET_KEY') 

    db.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)
    from apps.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
