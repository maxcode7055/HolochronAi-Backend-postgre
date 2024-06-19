# apps/routes/health.py
from flask import Blueprint, jsonify
from apps import db
from sqlalchemy import text
health_bp = Blueprint('health', __name__)

@health_bp.route('/health', methods=['GET'])
def health_check():
    try:
        with db.engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return jsonify({'status': 'ok', 'message': 'PostgreSQL database connected successfully!'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error connecting to PostgreSQL database: {str(e)}'})
