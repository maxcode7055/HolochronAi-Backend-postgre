from flask import Blueprint, jsonify, g, request, current_app, render_template
from apps.services.users import *
from apps.utils.helper import hash_password, verify_password

from pymongo.errors import PyMongoError
from bson import ObjectId
from apps.services.workspace_services import *
# from apps.middleware.jwt_auth import required_token
from apps.services.user_workspaces_services import *
from apps.services.characters_services import *
# from apps.services.chat_history import *
# from apps.services.scenes_services import *
import logging
from apps.tasks import send_email
from flask_jwt_extended import create_access_token, decode_token, JWTManager
from apps.utils.threading_helper import BLACKLIST, add_to_blacklist
# from line_profiler import profile


users_bp = Blueprint('users', __name__)

# @users_bp.route('/api/user/delete', methods=['GET'])
# @required_token
# def delete():
#     try:
#         session_data = getattr(g, 'session_data', None)
#         if not session_data:
#             return {"status": 301, "message": "Session data not found."}, 301

#         user_id = ObjectId(session_data['id'])
        
#         # Trial code starts here
#         token_jti = getattr(g, 'jti', None)
#         add_to_blacklist(token_jti)
     
#         # Trial code ends here

#         # Delete everything connected with the user

#         # Delete chat history
#         where = {"$or": [{"receiver_id": user_id}, {"sender_id": user_id}]}
        
#         chatdata = {  'deleted': True }
#         update_chat(where, {"$set":chatdata})
#         # Get all workspace ids associated with the user
#         workspace_ids = list(all_workspace_ids({"user_id": user_id, "deleted":False}))
        
#         if workspace_ids and len(workspace_ids)>0:
#             # Get all character ids associated with the workspaces or user
#             character_query = {
#                 "$or": [
#                     {"workspace_id": {"$in": workspace_ids}},
#                     {"user_id": user_id}
#                 ]
#             }
        
#             character_ids = list(get_all_characters_ids(character_query))
#             # Delete characters
#             if character_ids and len(character_ids)>0:
#                 update_characters({"_id": {"$in": character_ids}}, {"deleted":True})
#             update_workspace({"_id": {"$in": workspace_ids}}, {"$set":{"deleted":True}})
#             update_user_workspace({"user_id": user_id}, {"$set":{"deleted":True}})

        
#         result = update_user_profile({"_id": ObjectId(session_data["id"])}, {"deleted":True})
#         if result.modified_count:
#             return {"status": 200, "message": "Your account has been deleted successfully."}, 200
#         else:
#             return {"status": 301, "message": "Unable to perform this action right now."}, 301

#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301


def add(data):
        try:
            is_google_login = False
            is_microsoft_login = False
            if "is_google_login" in data:
                 is_google_login = data["is_google_login"]
            if "is_microsoft_login" in data:
                 is_microsoft_login = data["is_microsoft_login"]
            # user_exists = check_user_exists({"email":data['email'].lower()})
            # if user_exists:
            #     return False

            user_data = {
                'email': data['email'].lower(),
                'password':hash_password(data['password']),
                'name': data['name'].lower(),
                "is_google_login":is_google_login,
                "is_microsoft_login":is_microsoft_login,
                "chat_setting":25,
                "active":True,
                "deleted":False
            }
            insert_result = add_user(user_data)
            if insert_result.id:
                user_id = insert_result.id
                return user_id
            else:
                return False
        except Exception as e:
            return False
        
# def invite_users(data, workspace):
#         try:
#             user_ids = []
#             is_google_login = False
#             user_data = {  
#                     "is_google_login":is_google_login,
#                     "chat_setting":25,
#                     "active":False,
#                     "deleted":False
#             }
#             for email in data:
#                 user_data['email'] =  email.lower()
#                 insert_result = add_user(user_data)
                
#                 user_id = insert_result.inserted_id
#                 user_data = {
#                     'email': user_data['email'],
#                     "_id":str(insert_result.inserted_id)
#                 }
                
#                 token = create_access_token(identity=user_data, expires_delta=timedelta(hours=24))
                
#                 verification_link = f"{current_app.config['IMAGE_URL']}/accept-invite?token={token}"
#                 html_content = render_template('accept_invite.html',  verification_link=verification_link, workspace=workspace)
#                 sent  = send_email("Holochron Invite", user_data['email'], html_content)
#                 user_ids.append(user_id)
                
#             return user_ids
#         except Exception as e:
#             return False
           
        
# @users_bp.route('/api/user_details', methods=['GET'])
# @required_token
# def user_details():
    
#     session_data = getattr(g, 'session_data', None)
#     user_details = list(get_user_detail({"_id":ObjectId(session_data["id"])}))

#     if user_details and len(user_details):
#         return jsonify({"status":200,"error":False, "message":"","data":user_details[0]}), 200
#     else: 
#         return jsonify({"status":301,"error":True, "message":"","data":{}}), 301
    
    
# @users_bp.route('/api/update_profile', methods=['POST'])
# @required_token
# def update_profile():
    
#     session_data = getattr(g, 'session_data', None)
#     print("session_data")
#     print(session_data)
#     data = request.get_json()
    
#     for key, value in data.items():
#         if isinstance(value, bytes):
#             data[key] = value.decode('utf-8')
    
#     update_profile_result = update_user_profile({"_id": ObjectId(session_data["id"])}, data)
#     if update_profile_result.acknowledged:
#         user_details = list(get_user_detail({"_id": ObjectId(session_data["id"])}))
        
#         if user_details and "email" in user_details[0] and "name" in user_details[0] and "_id" in user_details[0] and "chat_setting" in user_details[0]:
#             data = {
#                 'email': user_details[0]["email"].lower(),
#                 'name': user_details[0]["name"],
#                 '_id': str(user_details[0]["_id"]),  
#                 'chat_setting': user_details[0]["chat_setting"]
#             }
#             return jsonify({"status": 200, "error": False, "message": "", "data": data}), 200
#         else:
#             return jsonify({
#                 "status": 301,
#                 "error": True,
#                 "message": "User details are incomplete",
#                 "data": []  
#             }), 301
#     else:
#         return jsonify({
#             "status": 301,
#             "error": True,
#             "message": "Unable to update user profile right now",
#             "data": []  
#         }), 301
    
# @users_bp.route('/api/get/collaborator', methods=['GET'])
# @required_token
# def users_list():
#     try:
#         session_data = getattr(g, 'session_data', None)
#         user_details = list(get_collaborator({"$and": [{"_id":{"$nin":[ObjectId(session_data["id"])]}},{"$or":[{"active":True},{"active":{"$exists":False}}]}, {"$or":[{"deleted":False},{"deleted":{"$exists":False}}]}]}, {"email":1, "_id":{ "$toString": "$_id" }, "name":1}))
#         if user_details and len(user_details):
#             return jsonify({"status":200,"error":False, "message":"","data":user_details}), 200
#         else: 
#             return jsonify({"status":301,"error":True, "message":"","data":[]}), 301  
#     except Exception as e:
#         return False
