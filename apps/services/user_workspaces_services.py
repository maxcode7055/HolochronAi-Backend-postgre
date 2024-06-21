from apps import db
from apps.models.user_workspace import UserWorkspace
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
# def get_all_user_workspaces(query, user_id):
#     try:
#         collection = get_collection()

#         pipeline = [
#             {"$match": query},
#             {"$sort": {"_id": -1}},
#             {
#                 "$lookup": {
#                     "from": "workspaces",
#                     "localField": "workspace_id",
#                     "foreignField": "_id",
#                     "as": "workspace_info"
#                 }
#             },
#             {
#                 "$unwind": "$workspace_info"
#             },
#             {
#                 "$lookup": {
#                     "from": "users",
#                     "localField": "workspace_info.collaborators",
#                     "foreignField": "_id",
#                     "as": "workspace_info.collaborators_detail",
#                     "pipeline":[
#                          {"$match":{'deleted': False}},
#                          {"$project":{'email': 1}}
#                     ]
#                 }
#             },
#             {
#                 "$addFields": {
#                     "workspace_info.role": {
#                         "$cond": {
#                             "if": {"$eq": ["$workspace_info.collaborators", user_id]},
#                             "then": "editor",
#                             "else": "admin"
#                         }
#                     },
#                     "workspace_info.workspace_unique_id": {
#                         "$ifNull": [
#                             "$workspace_info.workspace_unique_id",
#                             {"$concat": [
#                                 {"$toLower": {"$arrayElemAt": [{"$split": ["$workspace_info.workspace_name", " "]}, 0]}},
#                                 "_",
#                                 {"$toLower": {"$arrayElemAt": [{"$split": ["$workspace_info.workspace_name", " "]}, 1]}},
#                                 "-1234"
#                             ]}
#                         ]
#                     },
#                      "workspace_info.collaborators_emails": {
#                             "$map": {
#                                 "input": "$workspace_info.collaborators_detail",
#                                 "as": "collaborator",
#                                 "in": "$$collaborator.email"
#                             }
#                         },
#                 }
#             },
#             {
#                 "$project": {
#                     "_id": 0,
#                     "workspace_info": {
#                         "_id": {"$toString": "$workspace_info._id"},
#                         "workspace_name": 1,
#                         "settings": 1,
#                         "collaborators": "$workspace_info.collaborators_emails",
#                         "role": 1,
#                         "workspace_unique_id": 1
#                     }
#                 }
#             }
#         ]

        
#         workspace = collection.aggregate(pipeline)



#         # workspace = collection.find(query)
#         return workspace
#     except Exception as e:
#             return {"status": 301, "message": f"KeyError: {str(e)}"}, 301


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