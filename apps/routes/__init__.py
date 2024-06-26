# apps/routes/__init__.py
from flask import Blueprint

from .default_categories import default_categories_bp
from .auth import auth_bp
from .workspace import workspace_bp
from .health import health_bp
from .character import character_bp

routes_bp = Blueprint('routes', __name__)

routes_bp.register_blueprint(default_categories_bp)
routes_bp.register_blueprint(auth_bp)
routes_bp.register_blueprint(workspace_bp)
routes_bp.register_blueprint(character_bp)
# routes_bp.register_blueprint(health_bp, url_prefix='/')