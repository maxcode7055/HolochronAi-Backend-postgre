from apps.models import DefaultCategory
from apps import db
from sqlalchemy.orm import Query
from sqlalchemy import desc
def apply_filters(query: Query, model, filters: dict, sort_by: str = None, sort_order: str = 'asc') -> Query:

    # Apply filters
    for attr, value in filters.items():
        if hasattr(model, attr):
            query = query.filter(getattr(model, attr) == value)
    
    # Apply sorting
    if sort_by and hasattr(model, sort_by):
        if sort_order == 'desc':
            query = query.order_by(desc(getattr(model, sort_by)))
        else:
            query = query.order_by(getattr(model, sort_by))
    
    return query

def get_all_default_categories(query):
    try:
        characters = query.all()
        return characters
    except Exception as e:
            return {"status": 301, "message": f"KeyError: {str(e)}"}, 301


# def save_default_categories(data):
#     try:
#         collection = get_collection()
#         result = collection.insert_many(data)
#         return {"error": False, "data": result.inserted_ids}
#     except Exception as e:
#         return {"error": True, "message": f"Error: {str(e)}"}