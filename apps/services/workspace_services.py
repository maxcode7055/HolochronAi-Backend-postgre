from apps import db
from apps.models.workspaces import Workspace
from sqlalchemy import create_engine, Column, Integer, String, Boolean, or_, and_

def get_session():
    return db.session

      
   

# def get_collection():
#     try:
#         db = get_db()
#         return db['workspaces']
#     except Exception as e:
#                 return {"status": 301, "message": f"KeyError: {str(e)}"}, 301


# def check_workspace_exists(query):
#     try:
#         collection = get_collection()
       
#         workspace = collection.find_one(query)
#         return workspace is not None
#     except Exception as e:
#             return {"status": 301, "message": f"KeyError: {str(e)}"}, 301
        
# def check_existing_workspace(workspace_id):
#     try:
#         collection = get_collection()
#         if collection is None:
#             return False
        
#         workspace = collection.find_one({
#             "_id": ObjectId(workspace_id),
#             "deleted": False,
#             "active": True
#         })
#         return workspace is not None
#     except Exception as e:
#         logging.error(f"Error checking workspace existence: {str(e)}")
#         return False


# def get_workspace_detail(query):
#     try:
#         collection = get_collection()
#         workspace = collection.find_one(query)
#         return workspace
#     except Exception as e:
#             return {"status": 301, "message": f"KeyError: {str(e)}"}, 301


# def get_all_workspaces(query):
#     try:
#         collection = get_collection()
#         workspace = collection.find(query)
#         return workspace
#     except Exception as e:
#             return {"status": 301, "message": f"KeyError: {str(e)}"}, 301
 
    
def add_workspace(data):
    try:
            session = get_session()
            new_workspace = Workspace(
                workspace_name=data['workspace_name'],
                settings=data['settings'],
                created_at=data['created_at'],
                deleted=data['deleted'],
                active=data['active'],
                workspace_unique_id=data['workspace_unique_id'],
                is_default=data['default'],
                # collaborators=data['collaborators']
            )
            session.add(new_workspace)
            session.commit()
            new_workspace_dict = {c.key: getattr(new_workspace, c.key) for c in new_workspace.__table__.columns}
            return new_workspace_dict
    except Exception as e:
                return {"status": 301, "message": f"KeyError: {str(e)}"}, 301
            

# def delete_workspace(query):
#     try:
#         collection = get_collection()
#         return collection.find_one_and_delete(query)
        
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301
          
            
# def update_workspace(query, update_data):
#     try:
#         collection = get_collection()
        
#         update_result = collection.update_one(query, update_data, upsert=True)
        
#         return update_result.modified_count > 0  
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301
    
# def delete_all_workspaces(query):
#     try:
#         collection = get_collection()
#         return collection.delete_many(query)
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301
                