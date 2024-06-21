

from flask import Blueprint, request, jsonify, g, send_from_directory, current_app, url_for
import os
from apps.utils.helper import *
# from apps.middleware.jwt_auth import required_token
from apps.services.users import check_user_exists, add_user #, get_user_detail
from apps.services.characters_services import *
# from apps.services.user_workspaces_services import *
# from urllib.parse import urljoin
# from apps.services.knowledge_services import *
# from apps.services.scenes_services import *
# from apps.services.story_services import *
# from apps.utils.save_image_to_path import *
import datetime as dt
import json
import re

from bson import ObjectId
import uuid


character_bp = Blueprint('character', __name__, static_folder='uploads')
# class CharacterService: 

    
    # def get_characters():
    #     try:
    #         session_data = getattr(g, 'session_data', None)
    #         workspace_id = request.json.get('workspace_id') if request.content_type == 'application/json' else "all"

    #         query = {
    #             "$and": [
    #                 {"$or": [
    #                     {"user_id": ObjectId(session_data["id"])},
    #                     {"user_id": {"$exists": False}}
    #                 ]},
    #                 {"$or": [
    #                     {"deleted": False},
    #                     {"deleted": {"$exists": False}}
    #                 ]},
    #                 {"$or": [
    #                     {"active": True},
    #                     {"active": {"$exists": False}}
    #                 ]}
    #             ]
    #         }

    #         if workspace_id == "all":
    #             # Get all user workspaces
    #             workspaces = list(get_all_user_workspaces({"user_id": ObjectId(session_data['id'])}, ObjectId(session_data['id'])))

    #             # Extract workspace_info IDs
    #             workspace_info_ids = [
    #                 ObjectId(item['workspace_info']['_id'])
    #                 for item in workspaces if item and item.get('workspace_info')
    #             ]

    #             if workspace_info_ids:
    #                 query["$and"].append({"workspace_id": {"$in": workspace_info_ids}})
    #         else:
    #             query["$and"].append({"workspace_id": ObjectId(workspace_id)})

    #         # Get characters based on the constructed query
    #         characters = list(get_all_characters(query))

    #         if characters:
    #             return jsonify({"error": False, "message": "", "data": characters}), 200
    #         else:
    #             return jsonify({"error": True, "message": "No characters are added for selected workspaces yet.", "data": []}), 301

    #     except Exception as e:
    #         return jsonify({"error": True, "status": 301, "message": f"Error: {str(e)}"}), 301

    # @character_bp.route('/createCharacter', methods=['POST'])
    # @required_token
    # def createCharacter():
    #     try:
    #         session_data = getattr(g, 'session_data', None)
    #         if request.headers['Content-Type'] == 'application/json':
    #             data = request.get_json()
    #         else:
    #             data = request.form.to_dict()
                
    #         workspace_id = data.get('workspace_id', '')
    #         if not workspace_id:
    #             return jsonify({'status': 301, 'error': True, 'message': 'Please select a workspace.', 'data': []}), 301
    #         name = data.get('name', '')
    #         description = data.get('description', '')
    #         avatar = data.get('avatar', '')
    #         avatar_url = data.get('avatar_url', '')
    #         language = data.get('language', '')
    #         actions_state = data.get('actions_state', [])
    #         hobbies = data.get('hobbies', [])
    #         pronouns = data.get('pronouns', '')
    #         role = data.get('role', '')
    #         age = data.get('age', '')
    #         alternative_name = data.get('alternative_name', [])
            
            
    #         if not name:
    #             return jsonify({'status': 301, 'error': True, 'message': 'Name is required', 'data': []}), 301
    #         if not description:
    #             return jsonify({'status': 301, 'error': True, 'message': 'Description is required', 'data': []}), 301
    #         if not language:
    #             return jsonify({'status': 301, 'error': True, 'message': 'Language is required', 'data': []}), 301
    #         if not actions_state:
    #             return jsonify({'status': 301, 'error': True, 'message': 'Actions state is required', 'data': []}), 301
            
    #         avatar = data.get('avatar', '')
    #         avatar_url = data.get('avatar_url', '')            
    #         personality_traits = data.get('personality_traits', {
    #             'openness': 0,
    #             'meticulousness': 0,
    #             'extraversion': 0,
    #             'agreeableness': 0,
    #             'sensitivity': 0
    #         })
    #         dialouge_style = data.get('dialouge_style', {
    #         "adjectives": [],
    #         "colloquialism": [],
    #         "example_dailouge": "",
    #         "dialogue_dropdown": [],
    #         "dialogue_dropdown": [],
    #         })
    #         state_of_mind = data.get('state_of_mind',''),
    #         avatar_key = data.get('avatar_key', ''),
    #         long_term_memory = False
    #         node_based_story = False
    #         motivation = data.get('motivation', '')
    #         flaws = data.get('flaws', '')
    #         wikipedia_link = data.get('wikipedia_link', '')
    #         knowledge_filters = data.get('knowledge_filters', '')

    #         if not name:
    #             return jsonify({'status': 301, 'error': True, 'message': 'Name is required', 'data': []}), 301

    #         date = dt.datetime.now()
    #         timestamp = date.timestamp()
            
    #         character_data = {
    #             "name": name,
    #             "description": description,
    #             "language": language,
    #             "pronouns": pronouns,
    #             "role": role,
    #             "age": age,
    #             "alternative_name": alternative_name,
    #             "hobbies": hobbies,
    #             "actions_state": actions_state,
    #             "personality_traits": personality_traits,
    #             "dialouge_style": dialouge_style,
    #             "state_of_mind": state_of_mind,
    #             "avatar_key":avatar_key,
    #             "long_term_memory": long_term_memory,
    #             "node_based_story": node_based_story,
    #             "user_id": ObjectId(session_data['id']),
    #             "workspace_id" : ObjectId(workspace_id),
    #             "avatar":avatar,
    #             "avatar_url":avatar_url,
    #             # "knowledge_bank":[],
    #             "motivation" : motivation,
    #             "flaws" : flaws,
    #             "knowledge_filters" : knowledge_filters,
    #             "safety": {
    #             "profanity": None,
    #             "violence": None,
    #             "adult_topics": None,
    #             "substance_use": None,
    #             "Alcohol":None,
    #             "politics": None,
    #             "religion": None },
    #             "safety_status": False,
    #             "wikipedia_link": wikipedia_link,
    #             "wikipedia_link_status": False,
    #             "yaml_editor_status": False,
    #             "created_at": timestamp
    #         }
    #         if "personal_knowledge" in data:
    #             character_data['personal_knowledge'] = data['personal_knowledge']

            
    #         # Add character to the database
    #         result = add_characters_workspace(character_data)
    #         if result.inserted_id:
    #             if "common_knowledge" in data:
    #                 knowledge_ids = [ObjectId(id) for id in data['common_knowledge']]
    #                 saved = add_character_to_knowledge({"_id":{"$in":knowledge_ids}},{ "$addToSet": { characters: ObjectId(result.inserted_id) } })
    #                 removed = add_character_to_knowledge({"_id":{"$nin":knowledge_ids}},{ "$pull": { "characters": ObjectId(result.inserted_id) } })

    #             if "scenes" in data:
    #                 scenes_ids = [ObjectId(id) for id in data['scenes']]
    #                 saved = add_scenes_to_knowledge({"_id":{"$in":scenes_ids}},{ "$addToSet": { "characters": ObjectId(result.inserted_id) } })
    #                 removed = add_scenes_to_knowledge({"_id":{"$nin":scenes_ids}},{ "$pull": { "characters": ObjectId(result.inserted_id) } })

    #             characters = list(get_character_detail({"_id":result.inserted_id}))
    #             return jsonify({'status': 200, 'error': False, 'message': 'Character created successfully', 'data':characters[0] }), 200
    #         else:
    #             return jsonify({'status': 301, 'error': True, 'message': 'Unable to create character', 'data': []}), 301

    #     except Exception as e:
    #         return jsonify({'status': 301, 'error': True, 'message': f'Error: {str(e)}', 'data': []}), 301


    # @character_bp.route('/updateCharacter', methods=['POST'])
    # @required_token
    # def updateCharacter():
    #     try:
            
    #         session_data = getattr(g, 'session_data', None)
    #         if request.headers['Content-Type'] == 'application/json':
    #             data = request.get_json(silent=True)
    #         else:
    #             data = request.form.to_dict()
    #         if data is None:
    #             return jsonify({'status': 400, 'error': True, 'message': 'No JSON data provided', 'data': []}), 400
    #         character_id = data.get('character_id', '')

    #         if not character_id:
    #             return jsonify({'status': 301, 'error': True, 'message': 'Character ID is required', 'data': []}), 301

    #         updated_character_data = {}
    #         if "name" in data:
    #             updated_character_data['name'] = data['name']
    #         if "description" in data:
    #             updated_character_data['description'] = data['description']
    #         if "pronouns" in data:
    #             updated_character_data['pronouns'] = data['pronouns']
    #         if "role" in data:
    #             updated_character_data['role'] = data['role']
    #         if "age" in data:
    #             updated_character_data['age'] = data['age']
    #         if "alternative_name" in data:
    #             updated_character_data['alternative_name'] = data['alternative_name']
    #         if "hobbies" in data:
    #             updated_character_data['hobbies'] = data['hobbies']
    #         if "language" in data:
    #             updated_character_data['language'] = data['language']
    #         if "actions_state" in data:
    #             updated_character_data['actions_state'] = data['actions_state']
    #         if "personality_traits" in data:
    #             updated_character_data['personality_traits'] = data['personality_traits']
    #         if "state_of_mind" in data:
    #             updated_character_data['state_of_mind'] = data['state_of_mind']
    #         if "avatar_url" in data:
    #             updated_character_data['avatar_url'] = data['avatar_url']
    #         if "long_term_memory" in data:
    #             updated_character_data['long_term_memory'] = data['long_term_memory']
    #         if "node_based_story" in data:
    #             updated_character_data['node_based_story'] = data['node_based_story']
    #         if "motivation" in data:
    #             updated_character_data['motivation'] = data['motivation']
    #         if "flaws" in data:
    #             updated_character_data['flaws'] = data['flaws']
    #         if "dialouge_style" in data:
    #             updated_character_data['dialouge_style'] = data['dialouge_style']
    #         if "knowledge_filters" in data:
    #             updated_character_data['knowledge_filters'] = data['knowledge_filters']
    #         if "safety" in data:
    #             updated_character_data['safety'] = data['safety']
    #         if "safety_status" in data:
    #             updated_character_data['safety_status'] = data['safety_status']
    #         if "wikipedia_link" in data:
    #             updated_character_data['wikipedia_link'] = data['wikipedia_link']
    #         if "wikipedia_link_status" in data:
    #             updated_character_data['wikipedia_link_status'] = data['wikipedia_link_status']
    #         if "yaml_editor_status" in data:
    #             updated_character_data['yaml_editor_status'] = data['yaml_editor_status']
    #         if "avatar" in data:
    #             updated_character_data['avatar'] = data['avatar']
    #         if "wikipedia_link" in data:
    #             wikipedia_link = data['wikipedia_link']
    #             if wikipedia_link and not is_valid_wikipedia_url(wikipedia_link):
    #                 return jsonify({'status': 400, 'error': True, 'message': 'Invalid Wikipedia URL', 'data': []}), 400
    #             updated_character_data['wikipedia_link'] = wikipedia_link
            
                
    #         updated_character_data["user_id"] =  ObjectId(session_data['id'])
                
    #         if "personal_knowledge" in data:
    #             updated_character_data['personal_knowledge'] = data['personal_knowledge']

    #         if "common_knowledge" in data:
    #             knowledge_ids = [ObjectId(id) for id in data['common_knowledge']]
    #             saved = add_character_to_knowledge({"_id":{"$in":knowledge_ids}},{ "$addToSet": { "characters": ObjectId(character_id) } })
    #             removed = add_character_to_knowledge({"_id":{"$nin":knowledge_ids}},{ "$pull": { "characters": ObjectId(character_id) } })
    #         if "scenes" in data:
    #             scenes_ids = [ObjectId(id) for id in data['scenes']]
    #             saved = add_scenes_to_knowledge({"_id":{"$in":scenes_ids}},{ "$addToSet": { "characters": ObjectId(character_id) } })
    #             removed = add_scenes_to_knowledge({"_id":{"$nin":scenes_ids}},{ "$pull": { "characters": ObjectId(character_id) } })



    #         query = {"_id": ObjectId(character_id)}
    #         if not updated_character_data=={} : 
    #             result = update_characters(query, updated_character_data)
    #         if result.acknowledged:
    #             characters = list(get_character_detail(query))

    #             return jsonify({'status': 200, 'error': False, 'message': 'Character updated successfully', 'data': characters}), 200
    #         else:
    #             return jsonify({'status': 301, 'error': True, 'message': 'Unable to update character', 'data': []}), 301

    #     except Exception as e:
    #         return jsonify({'status': 500, 'error': True, 'message': f'Internal Server Error: {str(e)}', 'data': []}), 500
   
   
    # @character_bp.route('/characters/get-knowledge-list', methods=['POST'])
    # @required_token
    # def get_knowledge_list():
    #     try:
    #         data = request.get_json()
    #         session_data = getattr(g, 'session_data', None)
            
    #         if not "workspace_id" in data:
    #             return jsonify({"status": 301, "error": True, "message": "Please select a workspace.", "data": []}), 301
            
    #         query = {"user_id":ObjectId(session_data["id"]),"workspace_id":ObjectId(data.get('workspace_id'))}

    #         if "character_id" in data and data['character_id']!="":
    #             query = {
    #                 "user_id":ObjectId(session_data["id"]),
    #                 "workspace_id":ObjectId(data.get('workspace_id')), 
    #                 "$or":[{"characters": {"$nin":[ObjectId(data["character_id"])]}},  {"characters": {"$exists":False}}]
    #             }
    #         knowledge = get_all_knowledge(query)
    #         if knowledge:
    #             return jsonify({"status": 200, "error": False, "message": "", "data": list(knowledge)}), 200
    #         else:
    #             return jsonify({"status": 301, "error": True, "message": "No knowledge found.", "data": []}), 301
            
    #     except Exception as e:
    #         return jsonify({"status": 301, "error": True, "message": f"Error: {str(e)}", "data": []}), 301
    
    # @character_bp.route('/characters/get-scenes-list', methods=['POST'])
    # @required_token
    # def get_scenes_list():
    #     try:
    #         data = request.get_json()
    #         session_data = getattr(g, 'session_data', None)
            
    #         if not "workspace_id" in data:
    #             return jsonify({"status": 301, "error": True, "message": "Please select a workspace.", "data": []}), 301
            
    #         query = {"user_id":ObjectId(session_data["id"]),"workspace_id":ObjectId(data.get('workspace_id'))}

    #         if "character_id" in data and data['character_id']!="":
    #             query = {
    #                 "user_id":ObjectId(session_data["id"]),
    #                 "workspace_id":ObjectId(data.get('workspace_id')), 
    #                 "$or":[{"characters": {"$nin":[ObjectId(data["character_id"])]}},  {"characters": {"$exists":False}}]
    #             }
    #         scenes = list(get_character_scene(query))
    #         if scenes and len(scenes):
    #             return jsonify({"status": 200, "error": False, "message": "", "data": scenes}), 200
    #         else:
    #             return jsonify({"status": 301, "error": True, "message": "No knowledge found.", "data": []}), 301
            
    #     except Exception as e:
    #         return jsonify({"status": 301, "error": True, "message": f"Error: {str(e)}", "data": []}), 301
        

    # @character_bp.route('/characters', methods=['POST'])
    # @required_token
    # def get_character_detail():
    #     try:
    #         data = request.get_json()
    #         character_id = data.get('character_id')

    #         if character_id:
    #             character = get_all_characters({"_id": ObjectId(character_id)})
    #             if character:
    #                 return jsonify({"status": 200, "error": False, "message": "", "data": list(character)}), 200
    #             else:
    #                 return jsonify({"status": 301, "error": True, "message": "Character not found.", "data": []}), 301
    #         else:
    #             return jsonify({"status": 301, "error": True, "message": "Character ID not provided.", "data": []}), 301
    #     except Exception as e:
    #         return jsonify({"status": 301, "error": True, "message": f"Error: {str(e)}", "data": []}), 301
    

    # @character_bp.route('/character_names', methods=['POST'])
    # @required_token
    # def get_character_names():
    #     try:
    #         data = request.get_json()
    #         session_data = getattr(g, 'session_data', None)
            
    #         if not "workspace_id" in data:
    #             return jsonify({"status": 301, "error": True, "message": "Please select a workspace.", "data": []}), 301

    #         workspace_id = data.get('workspace_id')

    #         if workspace_id == "all":
    #             workspaces = list(get_all_user_workspaces({"user_id": ObjectId(session_data['id'])}, ObjectId(session_data['id'])))

    #             workspace_info_ids = [
    #                 ObjectId(item['workspace_info']['_id'])
    #                 for item in workspaces if item and item.get('workspace_info')
    #             ]

    #             query = {
    #                 "$and": [
    #                     {"$or": [
    #                         {"user_id": ObjectId(session_data["id"])},
    #                         {"user_id": {"$exists": False}}
    #                     ]},
    #                     {"$or": [
    #                         {"deleted": False},
    #                         {"deleted": {"$exists": False}}
    #                     ]},
    #                     {"$or": [
    #                         {"active": True},
    #                         {"active": {"$exists": False}}
    #                     ]}
    #                 ]
    #             }

    #             if workspace_info_ids:
    #                 query["$and"].append({"$or": [
    #                     {"workspace_id": {"$in": workspace_info_ids}},
    #                     {"workspace_id": {"$exists": False}}
    #                 ]})
    #         else:
    #             query = {
    #                 "$and": [
    #                     {"$or": [
    #                         {"user_id": ObjectId(session_data["id"])},
    #                         {"user_id": {"$exists": False}}
    #                     ]},
    #                     {"$or": [
    #                         {"workspace_id": ObjectId(workspace_id)},
    #                         {"workspace_id": {"$exists": False}}
    #                     ]},
    #                     {"$or": [
    #                         {"deleted": False},
    #                         {"deleted": {"$exists": False}}
    #                     ]},
    #                     {"$or": [
    #                         {"active": True},
    #                         {"active": {"$exists": False}}
    #                     ]}
    #                 ]
    #             }

    #         request_data = request.get_json(silent=True)
    #         search_name = request_data.get('search_name') if request_data else None

    #         if search_name is not None:
    #             if not isinstance(search_name, str):
    #                 return jsonify({"status": 400, "error": True, "message": "search_name must be a string.", "data": []}), 400
    #             query["name"] = {"$regex": search_name, "$options": "i"}
    #         elif "name" in query:
    #             del query["name"]

    #         characters = search_characters(query) if query else get_all_character_for_search(query, session_data["id"])

    #         if isinstance(characters, tuple) and len(characters) == 2:
    #             return jsonify(characters[0]), characters[1]

    #         for character in characters:
    #             character['_id'] = str(character['_id'])
    #             character['user_id'] = str(character['user_id']) if 'user_id' in character else None
    #             character['workspace_id'] = str(character['workspace_id']) if 'workspace_id' in character else None

    #         return jsonify({"status": 200, "error": False, "message": "All Characters data", "data": characters}), 200

    #     except Exception as e:
    #         return jsonify({"status": 500, "error": True, "message": f"Internal Server Error: {str(e)}", "data": []}), 500

    # @character_bp.route('/knowledge_bank_upload', methods=['POST'])
    # @required_token
    # def upload_file():
    #     if request.is_json:
    #         data = request.json
    #         character_id = data.get('character_id')
    #         knowledge_bank_id = data.get('knowledge_bank_id')
    #     else:
    #         character_id = request.form.get('character_id')
    #         knowledge_bank_id = request.form.get('knowledge_bank_id')
        
        
    #     if not character_id:
    #         return 'Please select a character.'
        
    #     character = list(get_all_characters({"_id": ObjectId(character_id)}))
        
    #     if not character:
    #         return 'Selected character is not found.'

    #     file = request.files.get('file')

    #     if not file:
    #         return 'No file uploaded'
        
    #     current_directory = os.path.dirname(os.path.abspath(__file__))
    #     parent_directory = os.path.dirname(current_directory)
    #     upload_folder = os.path.join(parent_directory, 'uploaded_files')

    #     if not os.path.exists(upload_folder):
    #         os.makedirs(upload_folder)

    #     filename = file.filename
    #     random_n = randon_number()
    #     file_path_dir = os.path.join(upload_folder, random_n+"_"+filename)
    #     file.save(file_path_dir)
    #     # file_path = "uploaded_files/" + filename
    #     file_path = "uploaded_files/" + random_n+"_"+filename
    #     date = dt.datetime.now()
    #     timestamp = date.timestamp()
    #     file_size = os.path.getsize(file_path_dir)
        
    #     where = {}
    #     data = {}
    #     arrayfilters = False
        
    #     if not knowledge_bank_id:
    #         c = {
    #             "id": str(uuid.uuid4()),
    #             "file_name": filename, 
    #             "is_available": True,
    #             "status": "inactive", 
    #             "timestamp": timestamp,
    #             "file_size": file_size,
    #             "file": file_path
    #         }
    #         characterData = []
    #         if "knowledge_bank" not in character[0]:
    #             characterData = [c]
    #             data = {'knowledge_bank': characterData}
    #         else:
    #             arrayfilters = None
    #             data = {"$push": {"knowledge_bank": c}}
    #         where = {"_id": ObjectId(character_id)}
            
    #     else:
    #         where = {"_id": ObjectId(character_id), "knowledge_bank.id": knowledge_bank_id}
    #         c = {
    #             "knowledge_bank.$[elem].file_name": filename, 
    #             "knowledge_bank.$[elem].is_available": True,
    #             "knowledge_bank.$[elem].status": "inactive", 
    #             "knowledge_bank.$[elem].timestamp": timestamp,
    #             "knowledge_bank.$[elem].file_size": file_size,
    #             "knowledge_bank.$[elem].file": file_path
    #         }
    #         data = {"$set": c}
    #         arrayfilters = [{"elem.id": knowledge_bank_id}]
    #     update_result = update_characters(where, data, arrayfilters)
        
    #     if not update_result:
    #         return 'Failed to update character'

    #     return jsonify({'status': 200, 'error': False, 'message': 'File uploaded and character knowledge bank updated successfully', 'data': [],"file_path":file_path}), 200

    
    # @character_bp.route('/api/connect-disconnect-knowledge-bank', methods=['POST'])
    # @required_token
    # def update_knowledge_bank():
    #     try:
    #         if request.content_type != 'application/json':
    #             return jsonify({'status': 301, 'error': True, 'message': 'Please send required parameter.', 'data': []}), 301
    #         if not request.json.get('status'):
    #             return jsonify({'status': 301, 'error': True, 'message': 'Please select one action to perform.', 'data': []}), 301
    #         if not request.json.get('character_id'):
    #             return jsonify({'status': 301, 'error': True, 'message': 'Please select one character.', 'data': []}), 301
    #         if not request.json.get('knowledge_bank_id'):
    #             return jsonify({'status': 301, 'error': True, 'message': 'Please send required parameter.', 'data': []}), 301

    #         character_id = request.json.get('character_id')
    #         knowledge_bank_id = request.json.get('knowledge_bank_id')
    #         status = request.json.get('status')

    #         where = {}
    #         data = {}
    #         result = False
    #         message = ""
            
    #         arrayfilers = False
    #         if status == "delete":
    #             message = "Deleted successfully."
    #             where = {'_id': ObjectId(character_id)}
    #             data = {'$pull': {'knowledge_bank': {'id': knowledge_bank_id}}}
    #         else:
    #             if status == "active":
    #                 message = "Connected successfully."
                    
    #                 # Deactivate all other knowledge banks
    #                 deactivate_where = {'_id': ObjectId(character_id)}
    #                 deactivate_data = {'$set': {'knowledge_bank.$[elem].status': 'inactive'}}
    #                 deactivate_array_filters = [{'elem.id': {'$ne': knowledge_bank_id}}]
    #                 update_knowledge_bank(deactivate_where, deactivate_data, deactivate_array_filters)

    #             else:
    #                 message = "Disconnected successfully."

    #             where = {"_id": ObjectId(character_id), "knowledge_bank.id": knowledge_bank_id}
    #             data = {"$set": {"knowledge_bank.$[elem].status": status}}
    #             arrayfilers = [{"elem.id": knowledge_bank_id}]

    #         result = update_knowledge_bank(where, data, arrayfilers)
            
    #         if result.acknowledged:
    #             return jsonify({'status': 200, 'error': False, 'message': message, 'data': []}), 200
    #         else:
    #             return jsonify({'status': 301, 'error': True, 'message': 'Unable to perform this action right now', 'data': []}), 301

    #     except Exception as e:
    #         return jsonify({"status": 301, "error": True, "message": f"Error: {str(e)}", "data": []}), 301

    
    
    # @character_bp.route('/deleteCharacter', methods=['POST'])
    # @required_token
    # def delete_character():
    #     data = request.get_json()

    #     if 'character_id' not in data:
    #         return jsonify({'status': 301, 'error': True, 'message': 'Please select a character', 'data': []}), 301

    #     character_id = data['character_id']

    #     if not check_characters_exists({'_id': ObjectId(character_id)}):
    #         return jsonify({'status': 404, 'error': True, 'message': 'Character does not exist', 'data': []}), 404

    #     deleted = delete_character({'_id': ObjectId(character_id)})
    #     if deleted:
    #         return jsonify({'status': 200, 'error': False, 'message': 'Character deleted successfully', 'character_id': character_id, 'data': []}), 200
    #     else:
    #         return jsonify({'status': 301, 'error': True, 'message': 'Please select a character', 'data': []}), 301


    # @character_bp.route('/duplicateCharacter', methods=['POST'])
    # @required_token
    # def duplicateCharacter():
    #     try:
    #         session_data = getattr(g, 'session_data', None)
    #         data = request.get_json()
    #         character_id = data.get('character_id', '')
    #         name = data.get('name', '')

    #         if not character_id:
    #             return jsonify({'status': 400, 'error': True, 'message': 'Character ID is required', 'data': []}), 400

    #         original_character = list(get_all_characters_for_duplicate({"_id": ObjectId(character_id)}))
    #         if not original_character or len(original_character) == 0:
    #             return jsonify({'status': 404, 'error': True, 'message': 'Character not found', 'data': []}), 404

    #         original_character = original_character[0]
    #         new_character_data = original_character.copy()
    #         new_character_data.pop('_id')
    #         new_character_data['name'] = name if name else f"{original_character['name']} (Copy)"
    #         new_character_data['created_at'] = dt.datetime.utcnow()
    #         new_character_data['user_id'] = ObjectId(session_data['id'])

    #         if 'workspace_id' in original_character:
    #             new_character_data['workspace_id'] = original_character['workspace_id']
            
    #         result = add_characters_workspace(new_character_data)
    #         if result.inserted_id:
    #             new_character = get_character_by_id(result.inserted_id)
    #             if new_character:
    #                 new_character['_id'] = str(new_character['_id'])
    #                 new_character['user_id'] = str(new_character['user_id'])
    #                 if 'workspace_id' in new_character:
    #                     new_character['workspace_id'] = str(new_character['workspace_id'])

    #                 original_character_id = str(original_character['_id'])
    #                 new_character_id = str(new_character['_id'])

    #                 scenes_exist = check_scenes_exists({"characters": ObjectId(original_character_id)})
    #                 if scenes_exist:
    #                     update_scene_result = update_scene_characters(original_character_id, new_character_id)
    #                 else:
    #                     print("No scenes found for the original character")
    #                 knowledge_exists = check_knowledge_exists({'user_id': ObjectId(session_data['id']), 'workspace_id': ObjectId(original_character['workspace_id']), 'characters': ObjectId(original_character_id)})
    #                 if knowledge_exists:
    #                     update_knowledge_result = update_knowledge_characters(original_character_id, new_character_id)
    #                 else:
    #                     print("No knowledge entries found for the original character")
                        
    #                 stories_exist = check_story_exists({"characters": ObjectId(original_character_id)})
    #                 if stories_exist:
    #                     update_story_result = update_story_characters(original_character_id, new_character_id)
    #                     print(f"Update Story Result: {update_story_result}")
    #                 else:
    #                     print("No story entries found for the original character")

    #                 return jsonify({'status': 200, 'error': False, 'message': 'Character duplicated successfully', 'data': new_character}), 200

    #         return jsonify({'status': 500, 'error': True, 'message': 'Unable to duplicate character', 'data': []}), 500

    #     except Exception as e:
    #         return jsonify({'status': 500, 'error': True, 'message': f'Internal Server Error: {str(e)}', 'data': []}), 500
    
    # @character_bp.route('/uploads/<path:filename>')
    # def uploaded_file(filename):
    #     return send_from_directory(character_bp.static_folder, filename)

    # @character_bp.route('/upload-image', methods=['POST'])
    # def upload_image():
    #     if 'image_name' not in request.files:
    #         return jsonify({'error': 'No image part in the request'}), 400
        
    #     file = request.files['image_name']
    #     old_image_name = request.form.get('old_image_name') 

    #     if file.filename == '':
    #         return jsonify({'error': 'No selected file'}), 400
        
    #     if file and allowed_file(file.filename):
    #         if old_image_name is not None:
    #             delete_image_from_path(old_image_name)
            
    #         filename = save_image_to_path(file)
    #         if filename:
    #             return jsonify({'image_name': filename}), 200
    #         else:
    #             return jsonify({'error': 'Failed to save the file'}), 500
    #     else:
    #         return jsonify({'error': 'File type not allowed'}), 400

# def check_knowledge_exists(query):
#     try:
#         knowledge_entries = get_all_knowledge(query)
#         return len(list(knowledge_entries)) > 0
#     except Exception as e:
#         print(f"Error checking knowledge entries: {str(e)}")
#         return False
    
# def check_scenes_exists(query):
#     try:
#         scenes = get_all_scenes(query)

#         return len(list(scenes)) > 0
#     except Exception as e:
#         print(f"Error checking scenes: {str(e)}")
#         return False

# def check_story_exists(query):
#     try:
#         stories = get_story_detail(query)
#         return bool(stories)
#     except Exception as e:
#         print(f"Error checking story existence: {str(e)}")
#         return False

# def update_scene_characters(original_character_id, new_character_id):
#     try:
#         update_result = update_many_scenes(
#             {"characters": ObjectId(original_character_id)},
#             {"$addToSet": {"characters": ObjectId(new_character_id)}}
#         )
#         if update_result.modified_count == 0:
#             return {"status": 200, "message": "No scenes found for the original character"}

#         return {"status": 200, "message": "Scene characters updated successfully"}
#     except Exception as e:
#         return {"status": 500, "message": f"Error: {str(e)}"}

# def update_knowledge_characters(original_character_id, new_character_id):
#     try:
#         update_result = update_many_knowledge(
#             {"characters": ObjectId(original_character_id)},
#             {"$addToSet": {"characters": ObjectId(new_character_id)}}
#         )
#         if update_result.modified_count == 0:
#             return {"status": 200, "message": "No knowledge entries found for the original character"}

#         return {"status": 200, "message": "Knowledge characters updated successfully"}
#     except Exception as e:
#         return {"status": 500, "message": f"Error: {str(e)}"}
    
# def update_story_characters(original_character_id, new_character_id):
#     try:
#         update_result = update_many_story(
#             {"characters": ObjectId(original_character_id)},
#             {"$addToSet": {"characters": ObjectId(new_character_id)}}
#         )
#         if update_result.modified_count > 0:
#             return {"status": 200, "message": "Story characters updated successfully"}
#         else:
#             return {"status": 200, "message": "No stories found for the original character"}
#     except Exception as e:
#         return {"status": 500, "message": f"Error: {str(e)}"}

# def is_valid_wikipedia_url(url):
#     wikipedia_pattern = r'^https?://(?:www\.)?en\.wikipedia\.org/wiki/[^/]+$'
#     return bool(re.match(wikipedia_pattern, url))

def create_default_character(workspace_id):
    try: 
        
        date = dt.datetime.now()
        timestamp = date.timestamp()
        characters =  [
            {
                "workspace_id":workspace_id,

                "name": "Elara Moonwhisper",
                "avatar": "Elara_Moonwhisper.webp",
                "description": "Elara Moonwhisper is a venerable elf, her age hidden beneath the timeless grace of her ethereal features. Her long silver hair cascades down her back like a waterfall of moonlight, adorned with delicate silver vines and tiny crystal stars. Her eyes, pools of deep azure, hold the wisdom of centuries past, twinkling with an otherworldly glow that seems to draw you into their depths. Elara's attire consists of flowing robes woven from the finest celestial silk, shimmering with enchantments that seem to dance in the light.As a guardian of the ancient knowledge of the realms, Elara exudes an aura of tranquility and power, her presence calming even the most troubled souls. She speaks in a melodic voice, each word carrying the weight of ages and resonating with the magic that flows through her veins. With a gentle smile, she offers guidance to those who seek her counsel, her words weaving tales of legends long forgotten and destinies yet to unfold.",
                "language": "English",
                "actions_state": ["Run","Walk"],
                "personality_traits": {
                        "openness": 0,
                        "meticulousness": 1,
                        "extraversion": 3,
                        "agreeableness": 2,
                        "sensitivity": 3
                    },
                "state_of_mind": ["Sad"],
                # "knowledge_cognition": {"personal":[], "common":[]},
                "character_scenes": [],
                "long_term_memory":False,
                "node_based_story":False,
                'deleted':False,
                'active':True,
                "configure_avatar":"",
                "knowledge_bank":"",
                "memory" :[],
                "settings":{},
                "safety": {
                "profanity": None,
                "violence": None,
                "adult_topics": None,
                "substance_use": None,
                "Alcohol":None,
                "politics": None,
                "religion": None },
                "safety_status": False,
                "wikipedia_link": "",
                "wikipedia_link_status": False,
                "yaml_editor_status": False,
                "dialogue_structure":"",
                "personal_knowledge":"",
                "created_at": timestamp
            },
            {
                "workspace_id":workspace_id,
                "name": "Aurora Dreamweaver",
                "avatar": "Aurora_Dreamweaver.webp",
                "description": "Dr. Aurora Dreamweaver is a renowned dream interpreter and nightmare therapist, revered for her deep understanding of the human psyche and her ability to decipher the enigmatic language of dreams. With her ethereal presence and piercing gaze, she exudes an aura of tranquility and wisdom that instantly puts her clients at ease. Her office is a sanctuary, adorned with tapestries depicting mystical landscapes and shelves lined with ancient tomes on dream symbolism. Dr. Dreamweaver possesses a keen intuition that allows her to delve into the depths of her clients' subconscious minds, unraveling the hidden meanings behind their dreams and nightmares. She believes that dreams are windows into the soul, revealing unspoken desires, fears, and unresolved conflicts. With compassion and insight, she guides her clients on a transformative journey of self-discovery, helping them to confront their inner demons and embrace their true selves.",
                "language": "English",
                "actions_state": ["Run","Walk"],
                "personality_traits": {
                        "openness": 0,
                        "meticulousness": 1,
                        "extraversion": 3,
                        "agreeableness": 2,
                        "sensitivity": 3
                    },
                "state_of_mind": ["Sad"],
                # "knowledge_cognition": {"personal":[], "common":[]},
                "character_scenes": [],
                "long_term_memory":False,
                "node_based_story":False,
                'deleted':False,
                'active':True,
                "configure_avatar":"",
                "knowledge_bank":"",
                "memory" :[],
                "settings":{},
                "safety": {
                "profanity": None,
                "violence": None,
                "adult_topics": None,
                "substance_use": None,
                "politics": None,
                "Alcohol":None,
                "religion": None },
                "safety_status": False,
                "hobbies" :[],
                "pronouns" :None,
                "role" :None,
                "age" :None,
                "alternative_name" :[],
                "motivation" :None,
                "flaws" :None,
                "wikipedia_link": "",
                "wikipedia_link_status": False,
                "yaml_editor_status": False,
                "dialogue_structure":"",
                "personal_knowledge":"",
                "created_at": timestamp
            },
            {
                "workspace_id":workspace_id,
                "name": "Alexander 'Alex' Pierce",
                "avatar": "Alexander_Alex_Pierce.webp",
                "description": "Alexander 'Alex' Pierce is a dynamic and forward-thinking entrepreneur with a knack for turning ideas into successful ventures. With a magnetic personality and a sharp business acumen, Alex exudes confidence and determination in everything they do. Their journey into the world of startups began with a passion for innovation and a relentless drive to bring change to industries ripe for disruption.Alex possesses a keen eye for spotting market gaps and opportunities, coupled with the ability to rally a team around a shared vision. Their leadership style is characterized by a perfect blend of ambition and empathy, inspiring others to push beyond their limits and achieve greatness. With a track record of launching and scaling startups across various sectors, Alex has garnered respect and admiration within the entrepreneurial community.Despite facing numerous challenges along the way, Alex remains undeterred, viewing obstacles as opportunities for growth and learning. Their resilience and adaptability have been instrumental in navigating the unpredictable terrain of entrepreneurship, propelling them towards continued success and recognition as a visionary leader in the startup ecosystem.",
                "language": "English",
                "actions_state": ["Run","Walk"],
                "personality_traits": {
                        "openness": 0,
                        "meticulousness": 1,
                        "extraversion": 3,
                        "agreeableness": 2,
                        "sensitivity": 3
                    },
                "state_of_mind": ["Sad"],
                # "knowledge_cognition": {"personal":[], "common":[]},
                "character_scenes": [],
                "long_term_memory":False,
                "node_based_story":False,
                'deleted':False,
                'active':True,
                "configure_avatar":"",
                "knowledge_bank":"",
                "memory" :[],
                "settings":{},
                "safety": {
                "profanity": None,
                "violence": None,
                "adult_topics": None,
                "substance_use": None,
                "politics": None,
                "Alcohol":None,
                "religion": None },
                "safety_status": False,
                "hobbies" :[],
                "pronouns" :None,
                "role" :None,
                "age" :None,
                "alternative_name" :[],
                "motivation" :None,
                "flaws" :None,
                "wikipedia_link": "",
                "wikipedia_link_status": False,
                "yaml_editor_status": False,
                "dialogue_structure":"" ,
                "personal_knowledge":"",
                "created_at": timestamp    
            },
            {
                "workspace_id":workspace_id,
                "name": "Cassandra 'Cass' Ryder",
                "avatar": "Cassandra_Cass_Ryder.webp",
                "description": "Cassandra 'Cass' Ryder is a seasoned investigator renowned for her expertise in unraveling the tangled webs of conspiracy theories. With a doctorate in psychology and a background in forensic science, Cass brings a unique blend of analytical rigor and empathetic understanding to her work. Her sharp intellect and keen eye for detail make her a formidable opponent for even the most entrenched myths and misinformation.Cass is driven by a deep commitment to the truth, believing that uncovering the facts is essential for preserving the fabric of society. Despite facing skepticism and resistance from those who cling to their beliefs, she remains undeterred in her pursuit of clarity and justice.Outside of her work, Cass enjoys quiet moments of reflection in her cozy apartment, surrounded by stacks of books and her trusty laptop. She finds solace in the pursuit of knowledge, always eager to delve deeper into the mysteries that captivate her curious mind.",
                "language": "English",
                "actions_state": ["Run","Walk"],
                "personality_traits": {
                        "openness": 0,
                        "meticulousness": 1,
                        "extraversion": 3,
                        "agreeableness": 2,
                        "sensitivity": 3
                    },
                "state_of_mind": ["Sad"],
                # "knowledge_cognition": {"personal":[], "common":[]},
                "character_scenes": [],
                "long_term_memory":False,
                "node_based_story":False,
                'deleted':False,
                'active':True,
                "configure_avatar":"",
                "knowledge_bank":"",
                "memory" :[],
                "settings":{},
                "safety": {
                "profanity": None,
                "violence": None,
                "adult_topics": None,
                "substance_use": None,
                "Alcohol":None,
                "politics": None,
                "religion": None },
                "safety_status": False,
                "hobbies" :[],
                "pronouns" :None,
                "role" :None,
                "age" :None,
                "alternative_name" :[],
                "motivation" :None,
                "flaws" :None,                
                "wikipedia_link": "",
                "wikipedia_link_status": False,
                "yaml_editor_status": False,
                "dialogue_structure":"",
                "personal_knowledge":"",
                "created_at": timestamp
            },
            {
                "workspace_id":workspace_id,
                "name": "Serena Skyheart",
                "avatar": "Serena_Skyheart.webp",
                "description": "Serena Skyheart, with her fiery red hair cascading down her back like a waterfall of flames, embodies the very essence of adventure. Her eyes, a striking shade of emerald green, sparkle with the excitement of exploration and the thrill of the unknown. With a confident stride and a mischievous grin, Serena exudes an aura of boundless energy and insatiable curiosity.Clad in sturdy leather boots and a weather-worn cloak adorned with patches from her countless travels, Serena carries herself with the grace of a seasoned explorer. Her trusty backpack, bulging with maps, journals, and artifacts collected from distant lands, is a testament to her insatiable thirst for discovery.But it's not just the physical world that Serena seeks to conquer; she is also a seeker of knowledge, constantly pushing the boundaries of her own mind and encouraging others to do the same. With a heart as brave as a lion and a spirit as free as the wind, Serena Skyheart inspires all who cross her path to embrace the unknown, seize every opportunity, and chase their wildest dreams with unwavering courage and determination.",
                "language": "English",
                "actions_state": ["Run","Walk"],
                "personality_traits": {
                        "openness": 0,
                        "meticulousness": 1,
                        "extraversion": 3,
                        "agreeableness": 2,
                        "sensitivity": 3
                    },
                "state_of_mind": ["Sad"],
                # "knowledge_cognition": {"personal":[], "common":[]},
                "character_scenes": [],
                "long_term_memory":False,
                "node_based_story":False,
                'deleted':False,
                'active':True,
                "configure_avatar":"",
                "knowledge_bank":"",
                "memory" :[],
                "settings":{},
                "safety": {
                "profanity": None,
                "violence": None,
                "adult_topics": None,
                "substance_use": None,
                "politics": None,
                "Alcohol":None,
                "religion": None },
                "safety_status": False,
                "hobbies" :[],
                "pronouns" :None,
                "role" :None,
                "age" :None,
                "alternative_name" :[],
                "motivation" :None,
                "flaws" :None,
                "wikipedia_link": "",
                "wikipedia_link_status": False,
                "yaml_editor_status": False,
                "dialogue_structure":"",
                "personal_knowledge":"",
                "created_at": timestamp
            },
            {
                "workspace_id":workspace_id,
                "name": "Aurora Everbright",
                "avatar": "Aurora_Everbright.webp",
                "description": "Aurora Everbright, the embodiment of luminosity and vitality, radiates an aura of boundless energy and unyielding optimism. With her piercing gaze and warm smile, she captivates hearts and ignites flames of inspiration in those around her. As a transformational leader, Aurora believes in the untapped potential within every individual, and her mission is to awaken and nurture that potential, guiding others toward their true purpose and fulfillment.Driven by her unwavering belief in the power of growth and self-discovery, Aurora empowers others to break free from the shackles of self-doubt and societal norms, urging them to embrace their uniqueness and unleash their inner greatness. She leads by example, embodying authenticity, resilience, and unwavering faith in the human spirit.Aurora's magnetic presence and visionary leadership have transformed countless lives, creating ripple effects of positive change that reverberate far and wide. With her guidance, others embark on a journey of personal evolution, transcending limitations, and embracing their full potential.",
                "language": "English",
                "actions_state": ["Run","Walk"],
                "personality_traits": {
                        "openness": 0,
                        "meticulousness": 1,
                        "extraversion": 3,
                        "agreeableness": 2,
                        "sensitivity": 3
                    },
                "state_of_mind": ["Sad"],
                # "knowledge_cognition": {"personal":[], "common":[]},
                "character_scenes": [],
                "long_term_memory":False,
                "node_based_story":False,
                'deleted':False,
                'active':True,

                "configure_avatar":"",
                "knowledge_bank":"",
                "memory" :[],
                "settings":{},
                "safety": {
                "profanity": None,
                "violence": None,
                "adult_topics": None,
                "substance_use": None,
                "politics": None,
                "Alcohol":None,
                "religion": None },
                "safety_status": False,
                "hobbies" :[],
                "pronouns" :None,
                "role" :None,
                "age" :None,
                "alternative_name" :[],
                "motivation" :None,
                "flaws" :None,
                "wikipedia_link": "",
                "wikipedia_link_status": False,
                "yaml_editor_status": False,
                "dialogue_structure":"",
                "personal_knowledge":"",
                "created_at": timestamp
            },
        ]
       
        saved = save_multiple_characters(characters)
        
        return jsonify({"message": "Data inserted successfully!"}), 200
    except Exception as e:
        return {'error': True, 'message': str(e)}