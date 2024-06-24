from apps import db
from apps.models.user_workspace import UserWorkspace
from apps.models.workspaces import Workspace
from apps.models.workspace_collaborators import WorkspaceCollaborators
from apps.models.users import User
from sqlalchemy import create_engine, Column, Integer, String, Boolean, or_, and_
from sqlalchemy.orm import joinedload


def get_workspaces_filter():
    return  {UserWorkspace.deleted == False}
def get_characters_workspaces_filter(userid):
     return {UserWorkspace.user_id == userid}
     
def get_session():
    return db.session
# def get_collection():
#     try:
#         db = get_db()
#         return db['user_workspaces']
#     except Exception as e:
#                 return {"status": 301, "message": f"KeyError: {str(e)}"}, 301

# def user_workspaces_exists(query):
#     try:
#         collection = get_collection()
       
#         workspace = collection.find_one(query)
#         return workspace is not None
#     except Exception as e:
#             return {"status": 301, "message": f"KeyError: {str(e)}"}, 301

# def user_workspaces_detail(query):
#     try:
#         collection = get_collection()
#         workspaces = collection.find_one(query)
#         return workspaces
#     except Exception as e:
#             return {"status": 301, "message": f"KeyError: {str(e)}"}, 301
    
def get_all_user_workspaces(query, user_id):
    try:
        session = get_session()
        query = (
            session.query(UserWorkspace, Workspace, User, User.email, WorkspaceCollaborators)
            .join(Workspace, UserWorkspace.workspace_id == Workspace.id)
            .join(User, UserWorkspace.user_id == User.id)
            .outerjoin(WorkspaceCollaborators, WorkspaceCollaborators.workspace_id == Workspace.id)
            .filter(UserWorkspace.user_id == user_id)
            .filter(UserWorkspace.deleted == False)  # Filter for non-deleted user_workspaces
            .filter(Workspace.deleted == False)  # Filter for non-deleted workspaces
            .options(
                joinedload(UserWorkspace.user),
                joinedload(UserWorkspace.workspace)
            )
            .all()
        )
        
        # Transform query result into desired format
        user_workspace_details = []
        for user_workspace, workspace, user, collaborator_email, workspace_collaborators in query:
            # Extract collaborators' email addresses
            collaborators_emails = []
            collaborators_ids = False
            if workspace_collaborators:
                collaborators_ids = [collaborator.id for collaborator in workspace_collaborators]
                collaborators_emails = [collaborator.email for collaborator in workspace_collaborators]
            
            user_workspace_details.append({
                "_id": workspace.id,
                "workspace_name": workspace.workspace_name,
                "settings": workspace.settings,
                "role": "editor" if collaborators_ids and user_id in collaborators_ids else "admin",
                "collaborators": collaborators_emails,
                "workspace_unique_id":workspace.workspace_unique_id
            })

        return user_workspace_details
    except Exception as e:
            return {"status": 301, "message": f"KeyError: {str(e)}"}, 301


def user_workspaces_add(data):
    try:
        session = get_session()
        new_user_workspace = UserWorkspace(user_id=data['user_id'], workspace_id=data['workspace_id'], deleted=data['deleted'], active=data['active'])
        session.add(new_user_workspace)
        session.commit()
        return new_user_workspace  # Return the id of the newly inserted user

    except Exception as e:
                return {"status": 301, "message": f"KeyError: {str(e)}"}, 301
            
# def delete_all_user_workspaces(query):
#     try:
#         collection = get_collection()
#         return collection.delete_many(query)
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301
     
# def all_workspace_ids(query):
#     try:
#         collection = get_collection()
#         # collection.create_index([("workspace_id", 'ASCENDING'), ("_id", 'ASCENDING')])
#         # print("query0-----------------------------",query)
#         cursor = collection.find(query, {"workspace_id": 1, "_id": 0})
#         ids = [doc["workspace_id"] for doc in cursor]
#         return ids
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301


# def user_workspaces_delete(query):
#     try:
#         collection = get_collection()
#         deleted_workspace = collection.find_one_and_delete(query)
#         return deleted_workspace is not None
#     except Exception as e:
#         return False

# def user_workspaces_detail(query):
#     try:
#         collection = get_collection()
#         workspace = collection.find_one(query)
#         return workspace
#     except Exception as e:
#         return {"status": 301, "message": f"KeyError: {str(e)}"}, 301 

# def update_user_workspace(query, update_data):
    try:
        collection = get_collection()
        
        update_result = collection.update_one(query, update_data, upsert=True)
        
        return update_result.modified_count > 0  
    except Exception as e:
        return {"status": 301, "message": f"Error: {str(e)}"}, 301