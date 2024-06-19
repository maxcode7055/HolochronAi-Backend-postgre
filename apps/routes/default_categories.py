# apps/routes/default_categories.py
from flask import Blueprint, request, jsonify
from apps.models import DefaultCategory
from apps import db
from apps.services.default_categories_services import *

default_categories_bp = Blueprint('default_categories', __name__)

@default_categories_bp.route('/default_categories', methods=['GET'])
def get():
    try:
        filters = {}
        query = DefaultCategory.query
        sort_by = 'id'
        sort_order = 'desc'
        query = apply_filters(query, DefaultCategory, filters, sort_by, sort_order)
        default_categories_data = get_all_default_categories(query)
        if default_categories_data and len(default_categories_data)>0:
            return jsonify({"status": 200, "error": False, "message": "All Default Categories data", "data": [{'id': default_category.id, 'name': default_category.name} for default_category in default_categories_data]}), 200
        else:
            return jsonify({"status": 301, "error": True, "message": "No Default Categories found.", "data": []}), 301
    except Exception as e:
        return jsonify({"status": 500, "error": True, "message": f"Internal Server Error: {str(e)}", "data": []}), 500

# @default_categories_bp.route('/default_categories', methods=['POST'])
# def add():
#     data = request.json
#     default_category = DefaultCategory(name=data['name'])
#     db.session.add(default_category)
#     db.session.commit()
#     return jsonify({'message': 'Category added successfully'}), 201


def add_default_categories():
    try:
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
    except Exception as e:
        print(f"Internal Server Error: {str(e)}")