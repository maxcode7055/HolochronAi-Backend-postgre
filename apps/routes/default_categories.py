# apps/routes/default_categories.py
from flask import Blueprint, request, jsonify
from apps.models import DefaultCategory
from apps import db

default_categories_bp = Blueprint('default_categories', __name__)

@default_categories_bp.route('/default_categories', methods=['GET'])
def get():
    default_categories_data = DefaultCategory.query.all()
    return jsonify([{'id': default_category.id, 'name': default_category.name} for default_category in default_categories_data])

@default_categories_bp.route('/default_categories', methods=['POST'])
def add():
    data = request.json
    default_category = DefaultCategory(name=data['name'])
    db.session.add(default_category)
    db.session.commit()
    return jsonify({'message': 'Category added successfully'}), 201

def add_default_categories():
    if DefaultCategory.query.count() == 0:
        default_categories = [
                {"name":"Person"},
                {"name":"Location"},
                {"name":"Date"},
                {"name":"Time"},
                {"name":"Organisation"},
                {"name":"Percent"},
                {"name":"Money"},
                {"name":"Quantity"},
                {"name":"Numeral"}
        ]
        db.session.bulk_insert_mappings(DefaultCategory, default_categories)
        db.session.commit()
        return True