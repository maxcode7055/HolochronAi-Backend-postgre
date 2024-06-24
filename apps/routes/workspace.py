
from flask import Blueprint, request, jsonify, g
from apps.services.workspace_services import *
from apps.services.user_workspaces_services import *
from apps.services.characters_services import *
from apps.routes.character import create_default_character
from apps.utils.helper import randon_number, join_string_by_under_score
from apps.services.users import *
from apps.routes.users import *

import json
import datetime 
from apps.middleware.jwt_auth import required_token
from apps.tasks import send_email, send_multiple_email

workspace_bp = Blueprint('workspace', __name__)

# class CustomEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, ObjectId):
#             return str(obj)
#         return json.JSONEncoder.default(self, obj)
    
    
def create_default_workspace():
    try: 
        workspace_unique_id  = join_string_by_under_score('Holochron AI Demo') + "-" +randon_number()
        workspace_data = { 
            'workspace_name': 'Holochron AI Demo',
            'settings': {
                'theme': 'light',
                'notifications': 'enabled',
                'layout': 'default'
            },
            'created_at': datetime.datetime.now(),
            'deleted':False,
            'active':True,
            "workspace_unique_id":workspace_unique_id,
            "default":False
        }
        
        result = add_workspace(workspace_data)
        if result['id']:
            create_default_character(result['id'])
            return result['id']
        else:
            return False
    except Exception as e:
        return {'error': True, 'message': str(e)}

    
class WorkspaceService:
    
#     @workspace_bp.route('/createWorkspace', methods=['POST'])
    
#     @required_token
#     def createWorkspace():
#         try:
            
#             session_data = getattr(g, 'session_data', None)
#             data = request.get_json()
#             if 'workspace_name' not in data:
#                 return jsonify({"error":True, 'message': 'Workspace name is required'}), 301
#             workspace_name = data['workspace_name']
#             if check_workspace_exists({'workspace_name':workspace_name}):
#                 return jsonify({"error":True, 'message': 'Workspace already exists'}), 301
#             else: 
#                 workspace_unique_id  = join_string_by_under_score(workspace_name) + "-" +randon_number()
                
#                 result = add_workspace({
#                         'workspace_name':workspace_name,
#                         "workspace_unique_id":workspace_unique_id,
#                         "default":False,
#                         "created_at":datetime.datetime.now(),
#                         "deleted":False,
#                         "active":True,
#                         "collaborators":[]
#                         })
                
#                 if result.acknowledged:
#                     user_workspace_data = {
#                         'user_id': ObjectId(session_data['id']),
#                         'workspace_id': result.inserted_id,
#                         'deleted':False,
#                         'active':True,
#                     }
#                     user_workspaces_add(user_workspace_data)
#                     return jsonify({"error":False,'message': 'Workspace created successfully', 'workspace_name': workspace_name}), 200
#                 else:
#                     return jsonify({"error":True, 'message': 'Unable to add workspace right now'}), 301
               
#         except Exception as e:
#             return jsonify({"error":True, "status": 301, "message": f"Error: {str(e)}"}), 301


    @workspace_bp.route('/workspaces', methods=['GET'])
    @required_token
    def get_workspaces():
        try:
            session_data = getattr(g, 'session_data', None)
            user_id = session_data.get('id')
            # Filter to get workspaces where the user is either the owner or collaborator, and not deleted
            query = get_workspaces_filter()
            workspaces = get_all_user_workspaces(query, user_id)
            if workspaces and len(workspaces)>0:
                return jsonify({"error": False, "message": "", "data": workspaces}), 200
            else:
                return jsonify({"error": True, "message": "No workspace found", "data": []}), 200
        
        except Exception as e:
            return jsonify({"error": True, "status": 301, "message": f"Error: {str(e)}"}), 301


#     @workspace_bp.route('/deleteWorkspace', methods=['POST'])
#     @required_token
#     def delete_workspace():
#         try:
#             data = request.get_json()
#             if 'workspace_id' not in data:
#                 return jsonify({'status': 400, 'error': True, 'message': 'Please select a workspace', 'data': []}), 400
            
#             session_data = getattr(g, 'session_data', None)

#             deleted = user_workspaces_delete({'workspace_id': ObjectId(data['workspace_id']), "user_id":ObjectId(session_data['id'])})
#             if deleted:
#                 # these entries should be in celery server
#                 delete_all_workspaces({"_id":ObjectId(data['workspace_id'])})
#                 delete_all_characters({"workspace_id":ObjectId(data['workspace_id'])})
#                 # these entries should be in celery server ends

#                 return jsonify({'status': 200, 'error': False, 'message': 'Workspace deleted successfully', 'workspace_id': data['workspace_id'], 'data': []}), 200
#             else:
#                 return jsonify({'status': 400, 'error': True, 'message': 'Failed to delete workspace', 'data': []}), 400
           
#         except Exception as e:
#             return jsonify({"status": 500, "error": True, "message": f"Error: {str(e)}"}), 500

        
#     @workspace_bp.route('/workspace/update', methods=['POST'])
#     @required_token
#     def edit_workspace():
#         try:
#             session_data = getattr(g, 'session_data', None)
#             data = request.get_json()

#             if 'workspace_id' not in data:
#                 return jsonify({"status": 301, 'error':True, 'message': 'Please select a workspace'}), 301
#             workspace_detail = get_workspace_detail({'_id': ObjectId(data['workspace_id'])})
#             if not workspace_detail:
#                 return jsonify({"status": 301, 'error':True, 'message': 'No such workspace exists'}), 301
#             datatobeupdate= {}
#             collaborator_ids = []
#             if 'collaborators' in data:
                
#                 existed_users = list(get_user_emails({"email":{"$in":data["collaborators"]}},{"email":1, "_id":1}))
              
#                 existed_emails = []
#                 new_emails = []
#                 if existed_users and len(existed_users):
#                     existed_emails = [elem["email"] for elem in existed_users]
#                     collaborator_ids = [elem["_id"] for elem in existed_users]
#                     datatobeupdate["collaborators"] = collaborator_ids

#                 if len(existed_emails) :
#                     new_emails = [elem for elem in data["collaborators"] if elem not in existed_emails]
#                 else :
#                     new_emails = data["collaborators"]
                      
#                 if len(new_emails)>0:
#                     new_ids = invite_users(new_emails, workspace_detail['workspace_name'])
                    
#                     for id in new_ids:
#                         datatobeupdate["collaborators"].append(id)
#                 if len(existed_emails)>0:
#                     html_content = render_template('add_collaborator.html', workspace=workspace_detail['workspace_name'])
#                     sent  = send_multiple_email("Holochron Invite", existed_emails, html_content)
            
#             if 'workspace_name' in data:
#                 datatobeupdate["workspace_name"] =  data['workspace_name']
#                 workspace_unique_id  = join_string_by_under_score(data['workspace_name']) + "-" +randon_number()
#                 datatobeupdate['workspace_unique_id'] =  workspace_unique_id
                
#             updated = update_workspace({'_id': ObjectId(data['workspace_id'])}, {"$set":datatobeupdate})
            

#             if updated:
#                 return jsonify({'error': False, 'message': 'Workspace updated successfully', 'workspace_id': str(data['workspace_id'])}), 200
#             else:
#                 return jsonify({'error': True, 'message': 'Failed to update workspace'}), 500

#         except Exception as e:
#             return jsonify({"error": True, "status": 500, "message": f"Error: {str(e)}"}), 500
        