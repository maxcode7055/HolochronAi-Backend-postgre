from apps import db
from apps.models.characters import Character
from apps.models.knowledge import Knowledge
from sqlalchemy import create_engine, text, func, case, and_, or_, join
import os

def get_session():
    return db.session

        
# def check_existing_character(character_id):
#     try:
#         collection = get_collection()
#         if collection is None:
#             return False

#         character = collection.find_one({
#             "_id": ObjectId(character_id),
#             "deleted": False,
#             "active": True
#         })
#         return character is not None
#     except Exception as e:
#         logging.error(f"Error checking character existence: {str(e)}")
#         return False




# def update_knowledge_bank(where, data, arrayfilters=False):
#     try:
#         collection = get_collection()  
#         if arrayfilters==False:
#              return collection.update_one(where, data)
#         else:
#             return collection.update_one(where, data, array_filters=arrayfilters)
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301  
       
# def get_character_by_id(character_id):
#     try:
#         collection = get_collection()
#         return collection.find_one({"_id": ObjectId(character_id)})
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301

def get_all_characters(query,params):
    try:
        session = get_session()
        base_query = """
            SELECT
            c.id,
            c.name,
            CASE
                WHEN c.avatar ~ '^https?://' THEN c.avatar
                ELSE COALESCE(CONCAT(:image_url, '/images/character_img/', c.avatar), CONCAT(:image_url, '/images/character_img/default_avatar.webp'))
            END AS avatar,
            CASE
                WHEN c.avatar_url ~ '^https?://' THEN c.avatar_url
                ELSE COALESCE(CONCAT(:image_url, '/images/character_img/', c.avatar_url), CONCAT(:image_url, '/images/character_img/default_avatar.webp'))
            END AS avatar_url,
            CASE
                WHEN c.yaml_file_path IS NOT NULL THEN CONCAT(:image_url, '/images/', c.yaml_file_path)
                ELSE NULL
            END AS yaml_file_path,
            c.description,
            c.pronouns,
            c.role,
            c.age,
            c.alternative_name,
            c.hobbies,
            c.stage_of_life,
            c.alternative_names,
            c.hobbies_and_interests,
            c.state_of_mind,
            c.avatar_key,
            c.language,
            c.actions_state,
            c.personality_traits,
            c.dialogue_style,
            c.long_term_memory,
            c.node_based_story,
            COALESCE(c.knowledge_bank, '[]') AS knowledge_bank,
            c.motivation,
            c.flaws,
            c.knowledge_filters,
            c.common_knowledge,
            c.personal_knowledge,
            c.safety,
            c.wikipedia_link,
            c.safety_status,
            c.wikipedia_link_status,
            c.yaml_editor_status,
            c.created_at
            FROM characters c
            WHERE TRUE
            {query}
        """
        # Execute the query
        result = session.execute(
            text(base_query),
            params
        ).fetchall()
        # Convert result to a list of dictionaries
        return [dict(row._mapping) for row in result]
    except Exception as e:
        return {"status": 301, "message": f"KeyError: {str(e)}"}, 301
# def get_character_detail(query):
#     try:
#         collection = get_collection()  
#         pipeline = [
#             {"$match": query},
#             {"$lookup": {
#                     "from": "knowledge",
#                     "localField": "_id",
#                     "foreignField": "characters",
#                     "as": "common_knowledge",
#                     "pipeline": [
#                         {
#                             "$project": {
#                                "_id": {"$toString": "$_id"},
#                                "knowledge_name":1,
#                                "knowledge_description":1,
#                                "knowledge_information":1
#                             }
#                         }
#                     ]
#                 }
#             },
#             {
#                 "$lookup": {
#                     "from": "scenes",
#                     "localField": "_id",
#                     "foreignField": "characters",
#                     "as": "attached_scenes",
#                     "pipeline": [
#                         {
#                             "$project": {
#                                "_id": {"$toString": "$_id"},
#                                "description":1,
#                                "scene_name":1,
#                                "scene_triggers":1
#                             }
#                         }
#                     ]
#                 }
#             },
#             {
#                 "$lookup": {
#                     "from": "story",
#                     "let": {"character_id": "$_id"},
#                     "pipeline": [
#                         {
#                             "$match": {
#                                 "$expr": {
#                                     "$and": [
#                                         {"$isArray": "$characters"},
#                                         {"$in": ["$$character_id", "$characters"]}
#                                     ]
#                                 }
#                             }
#                         },
#                         {
#                             "$project": {
#                                 "_id": {"$toString": "$_id"},
#                                 "name": 1,
#                                 "description": 1,
#                                 "typing_indicator_duration": 1,
#                                 "story_image": {
#                                     "$ifNull": [
#                                         {"$concat": [os.getenv("IMAGE_URL"), "/uploads/", "$story_image"]},
#                                         {"$concat": [os.getenv("IMAGE_URL"), "/images/character_img/", "default_avatar.webp"]}
#                                     ]
#                                 }
#                             }
#                         }
#                     ],
#                     "as": "attached_stories"
#                 }
#             },
#             {"$sort": {"created_at": -1, "_id": -1, "name":-1}},
#             {
#                 "$project": {
#                     "_id": {"$toString": "$_id"},
#                     "name": 1,
#                    "avatar":{

#                         "$cond": {
#                                 "if": {"$regexMatch": {"input": "$avatar", "regex": "^https?://"}},
#                                 "then": "$avatar",
#                                 "else": { "$ifNull": [{ "$concat": [ os.getenv("IMAGE_URL"), "/images/character_img/", "$avatar" ]}, { "$concat": [ os.getenv("IMAGE_URL"), "/images/character_img/", "default_avatar.webp" ]}] }
#                             }
#                         },
#                         "avatar_url": {
#                             "$cond": {
#                                 "if": {"$regexMatch": {"input": "$avatar_url", "regex": "^https?://"}},
#                                 "then": "$avatar_url",
#                                 "else": { "$ifNull": [{ "$concat": [ os.getenv("IMAGE_URL"), "/images/character_img/", "$avatar_url" ]}, { "$concat": [ os.getenv("IMAGE_URL"), "/images/character_img/", "default_avatar.webp" ]}] }
#                             }
#                         },
#                       "yaml_file_path":{"$ifNull": [{"$concat": [os.getenv("IMAGE_URL"), "/images/", "$yaml_file_path"]}, None]},
#                     "description": 1,
#                     "pronouns": 1,
#                     "role":1,
#                     "age":1,
#                     "alternative_name":1,
#                     "hobbies":1,
#                     "stage_of_life": 1,
#                     "alternative_names": 1,
#                     "hobbies_and_interests": 1,
#                     "state_of_mind": 1,
#                     "avatar_key": 1,
#                     "language": 1,
#                     "actions_state": 1,
#                     "personality_traits": 1,
#                     "dialouge_style":1,
#                     "long_term_memory": 1,
#                     "node_based_story": 1,
#                     "motivation":1,
#                     "flaws":1,
#                     "knowledge_filters":1,
#                     "knowledge_bank":1,
#                     "common_knowledge":1,
#                     "personal_knowledge":1,
#                     "safety":1,
#                     "wikipedia_link":1,
#                     "safety_status":1,
#                     "wikipedia_link_status":1,
#                     "yaml_editor_status":1,
#                     "created_at":1,
#                     "scenes":"$attached_scenes"
#                 }
#             }
#         ]

#         characters = list(collection.aggregate(pipeline))
        
#         # Check if characters is empty
#         if not characters:
#             return {"status": 404, "message": "No characters found"}

#         return characters
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}    
    
# def add_characters_workspace(data):
#     try:
#         collection = get_collection()
#         insert_result = collection.insert_one(data)
#         return insert_result
#     except Exception as e:
#                 return {"status": 301, "message": f"KeyError: {str(e)}"}, 301

# def update_characters(query, updated_data, arrayfilters=False):
#     try:
#         collection = get_collection()  # Assuming you have a function to get the collection
#         if arrayfilters==False:
#             print("in 1")
#             return collection.update_one(query, {"$set":updated_data}, upsert=True)
#         elif arrayfilters==None:
#             print("in 2")
#             return collection.update_one(query, updated_data)
#         else:
#             print("in 3")
#             return collection.update_one(query, updated_data, array_filters=arrayfilters)
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301

# def delete_character(query):
#     try:
#         collection = get_collection()
#         return collection.find_one_and_delete(query)
        
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301
    
def save_multiple_characters(data):
    try:
        session = get_session()
        session.bulk_insert_mappings(Character, data)
        session.commit()
        return True
    except Exception as e:
          return {"status": 301, "message": f"KeyError: {str(e)}"}, 301

# def get_all_characters_ids(query):
#     try:
#         collection = get_collection()
#         # collection.create_index([("workspace_id", 'ASCENDING'), ("user_id", 'ASCENDING')])
#         cursor = collection.find(query, {"_id": 1})
#         ids = [doc["_id"] for doc in cursor]
#         return ids
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301 

# def delete_all_characters(query):
#     try:
#         collection = get_collection()
#         return collection.delete_many(query)
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301

# def get_all_characters_for_duplicate(query):
#     try:
#         collection = get_collection()
#         pipeline = [
#             {"$match": query},
#             {
#                 "$addFields": {
#                     "knowledge_bank": {
#                         "$ifNull": ["$knowledge_bank", []]
#                     }
#                 }
#             },
#             {
#                 "$addFields": {
#                     "knowledge_bank.file": {
#                         "$cond": {
#                             "if": {
#                                 "$and": [
#                                     {"$gt": ["$knowledge_bank", None]},
#                                     {"$eq": [{"$type": "$knowledge_bank.file"}, "string"]},
#                                     {"$regexMatch": {"input": "$knowledge_bank.file", "regex": "^https?://"}}
#                                 ]
#                             },
#                             "then": "$knowledge_bank.file",
#                             "else": {
#                                 "$cond": {
#                                     "if": {"$and": [
#                                         {"$gt": ["$knowledge_bank", None]},
#                                         {"$eq": [{"$type": "$knowledge_bank.file"}, "string"]}
#                                     ]},
#                                     "then": {"$concat": [os.getenv("IMAGE_URL"), '/images/', '$knowledge_bank.file']},
#                                     "else": None
#                                 }
#                             }
#                         }
#                     }
#                 }
#             },
#             {
#                 "$group": {
#                     "_id": "$_id",
#                     "document": {"$first": "$$ROOT"},
#                     "knowledge_bank": {"$push": "$knowledge_bank"}
#                 }
#             },
#             {
#                 "$addFields": {
#                     "document.knowledge_bank": {
#                         "$cond": {
#                             "if": {"$eq": ["$knowledge_bank", [{}]]},
#                             "then": [],
#                             "else": {
#                                 "$cond": {
#                                     "if": {"$ne": ["$knowledge_bank", [{"file": None}]]},
#                                     "then": "$knowledge_bank",
#                                     "else": []
#                                 }
#                             }
#                         }
#                     }
#                 }
#             },
#             {
#                 "$replaceRoot": {
#                     "newRoot": "$document"
#                 }
#             },
#             {
#                 "$lookup": {
#                     "from": "workspaces",
#                     "localField": "_id",
#                     "foreignField": "characters",
#                     "as": "workspaces",
#                     "pipeline": [
#                         {
#                             "$project": {
#                                 "_id": {"$toString": "$_id"},
#                                 "workspace_name": 1,
#                             }
#                         }
#                     ]
#                 }
#             },
#             {
#                 "$lookup": {
#                     "from": "knowledge",
#                     "localField": "_id",
#                     "foreignField": "characters",
#                     "as": "common_knowledge",
#                     "pipeline": [
#                         {
#                             "$project": {
#                                 "_id": {"$toString": "$_id"},
#                                 "knowledge_name": 1,
#                                 "knowledge_description": 1,
#                                 "knowledge_information": 1
#                             }
#                         }
#                     ]
#                 }
#             },
#             {
#                 "$lookup": {
#                     "from": "scenes",
#                     "localField": "_id",
#                     "foreignField": "characters",
#                     "as": "attached_scenes",
#                     "pipeline": [
#                         {
#                             "$project": {
#                                 "_id": {"$toString": "$_id"},
#                                 "description": 1,
#                                 "scene_name": 1,
#                                 "scene_triggers": 1
#                             }
#                         }
#                     ]
#                 }
#             },
#             {
#                 "$lookup": {
#                     "from": "story",
#                     "let": {"character_id": "$_id"},
#                     "pipeline": [
#                         {
#                             "$match": {
#                                 "$expr": {
#                                     "$and": [
#                                         {"$isArray": "$characters"},
#                                         {"$in": ["$$character_id", "$characters"]}
#                                     ]
#                                 }
#                             }
#                         },
#                         {
#                             "$project": {
#                                 "_id": {"$toString": "$_id"},
#                                 "name": 1,
#                                 "description": 1,
#                                 "typing_indicator_duration": 1,
#                                 "story_image": {
#                                     "$ifNull": [
#                                         {"$concat": [os.getenv("IMAGE_URL"), "/uploads/", "$story_image"]},
#                                         {"$concat": [os.getenv("IMAGE_URL"), "/images/character_img/", "default_avatar.webp"]}
#                                     ]
#                                 }
#                             }
#                         }
#                     ],
#                     "as": "attached_stories"
#                 }
#             },
#             {"$sort": {"created_at": -1, "_id": -1, "name":-1}},
#             {
#                 "$project": {
#                     "_id": {"$toString": "$_id"},
#                     "name": 1,
#                     "avatar": {
#                         "$cond": {
#                             "if": {"$regexMatch": {"input": {"$toString": "$avatar"}, "regex": "^https?://"}},
#                             "then": "$avatar",
#                             "else": {"$ifNull": [{"$concat": [os.getenv("IMAGE_URL"), "/images/character_img/", "$avatar"]}, {"$concat": [os.getenv("IMAGE_URL"), "/images/character_img/", "default_avatar.webp"]}]}
#                         }
#                     },
#                     "avatar_url": {
#                         "$cond": {
#                             "if": {"$regexMatch": {"input": {"$toString": "$avatar_url"}, "regex": "^https?://"}},
#                             "then": "$avatar_url",
#                             "else": {"$ifNull": [{"$concat": [os.getenv("IMAGE_URL"), "/images/character_img/", "$avatar_url"]}, {"$concat": [os.getenv("IMAGE_URL"), "/images/character_img/", "default_avatar.webp"]}]}
#                         }
#                     },
#                      "yaml_file_path":{"$ifNull": [{"$concat": [os.getenv("IMAGE_URL"), "/images/", "$yaml_file_path"]}, None]},
#                     "description": 1,
#                     "pronouns": 1,
#                     "role":1,
#                     "age":1,
#                     "alternative_name":1,
#                     "hobbies":1,
#                     "stage_of_life": 1,
#                     "alternative_names": 1,
#                     "hobbies_and_interests": 1,
#                     "state_of_mind": 1,
#                     "avatar_key": 1,
#                     "language": 1,
#                     "actions_state": 1,
#                     "personality_traits": 1,
#                     "dialouge_style": 1,
#                     "long_term_memory": 1,
#                     "node_based_story": 1,
#                     "knowledge_bank": 1,
#                     "motivation": 1,
#                     "flaws": 1,
#                     "knowledge_filters": 1,
#                     "common_knowledge": 1,
#                     "personal_knowledge": 1,
#                     "safety": 1,
#                     "wikipedia_link": 1,
#                     "safety_status": 1,
#                     "wikipedia_link_status": 1,
#                     "yaml_editor_status": 1,
#                     "created_at":1,
#                     "scenes": "$attached_scenes",
#                     "workspace_id": 1 
#                 }
#             }
#         ]

#         characters = collection.aggregate(pipeline)
#         return list(characters) 
#     except Exception as e:
#         raise Exception(f"Error fetching characters: {str(e)}")

# def search_characters(query):
#     try:
#         collection = get_collection()
#         cursor = collection.find(query)
#         characters = list(cursor)

#         for character in characters:
#             character['_id'] = str(character['_id'])

#         if not characters:
#             return {"status": 404, "message": "No characters found."}, 404

#         return characters
#     except Exception as e:
#         return {"status": 500, "message": f"Internal Server Error: {str(e)}"}, 500
        
# def get_all_character_for_search(query, user_id):
#     try:
#         collection = get_collection()
#         pipeline = [
#             {"$match": {**query, "user_id": user_id}},
#             {"$sort": {"_id": -1}},
#             {
#                 "$addFields": {
#                     "knowledge_bank": {
#                         "$ifNull": ["$knowledge_bank", []]
#                     }
#                 }
#             },
#             {
#                 "$addFields": {
#                     "knowledge_bank.file": {
#                         "$cond": {
#                             "if": {
#                                 "$and": [
#                                     {"$gt": ["$knowledge_bank", None]},
#                                     {"$regexMatch": {"input": "$knowledge_bank.file", "regex": "^https?://"}}
#                                 ]
#                             },
#                             "then": "$knowledge_bank.file",
#                             "else": {
#                                 "$cond": {
#                                     "if": {"$gt": ["$knowledge_bank", None]},
#                                     "then": {"$concat": [os.getenv("IMAGE_URL"), '/images/', '$knowledge_bank.file']},
#                                     "else": None                                }
#                             }
#                         }
#                     }
#                 }
#             },
#             {
#                 "$group": {                    "_id": "$_id",
#                     "document": {"$first": "$$ROOT"},
#                     "knowledge_bank": {"$push": "$knowledge_bank"}
#                 }
#             },
#             {
#                 "$addFields": {
#                     "document.knowledge_bank": {
#                         "$cond": {
#                             "if": {"$eq": ["$knowledge_bank", [{}]]},
#                             "then": [],
#                             "else": {
#                                 "$cond": {
#                                     "if": {"$ne": ["$knowledge_bank", [{"file": None}]]},
#                                     "then": "$knowledge_bank",
#                                     "else": []
#                                 }
#                             }
#                         }
#                     }
#                 }
#             },
#             {
#                 "$replaceRoot": {
#                     "newRoot": "$document"
#                 }
#             },
#             {"$lookup": {
#                 "from": "knowledge",
#                 "localField": "_id",
#                 "foreignField": "characters",
#                 "as": "common_knowledge",
#                 "pipeline": [
#                     {
#                         "$project": {
#                             "_id": {"$toString": "$_id"},
#                             "knowledge_name": 1,
#                             "knowledge_description": 1,
#                             "knowledge_information": 1
#                         }
#                     }
#                 ]
#             }},
#             {"$lookup": {
#                 "from": "scenes",
#                 "localField": "_id",
#                 "foreignField": "characters",
#                 "as": "attached_scenes",
#                 "pipeline": [
#                     {
#                         "$project": {
#                             "_id": {"$toString": "$_id"},
#                             "description": 1,
#                             "scene_name": 1,
#                             "scene_triggers": 1
#                         }
#                     }
#                 ]
#             }},
#             {
#                 "$project": {
#                     "_id": {"$toString": "$_id"},
#                     "name": 1,
#                     "avatar": {
#                         "$cond": {
#                             "if": {"$regexMatch": {"input": "$avatar", "regex": "^https?://"}},
#                             "then": "$avatar",
#                             "else": {"$ifNull": [{"$concat": [os.getenv("IMAGE_URL"), "/images/character_img/", "$avatar"]}, {"$concat": [os.getenv("IMAGE_URL"), "/images/character_img/", "default_avatar.webp"]}]}
#                         }
#                     },
#                     "avatar_url": {
#                         "$cond": {
#                             "if": {"$regexMatch": {"input": "$avatar_url", "regex": "^https?://"}},
#                             "then": "$avatar_url",
#                             "else": {"$ifNull": [{"$concat": [os.getenv("IMAGE_URL"), "/images/character_img/", "$avatar_url"]}, {"$concat": [os.getenv("IMAGE_URL"), "/images/character_img/", "default_avatar.webp"]}]}
#                         }
#                     },
#                     "yaml_file_path":{"$ifNull": [{"$concat": [os.getenv("IMAGE_URL"), "/images/", "$yaml_file_path"]}, None]},
#                     "description": 1,
#                     "pronouns": 1,
#                     "role":1,
#                     "age":1,
#                     "alternative_name":1,
#                     "hobbies":1,
#                     "stage_of_life": 1,
#                     "alternative_names": 1,
#                     "hobbies_and_interests": 1,
#                     "state_of_mind": 1,
#                     "avatar_key": 1,
#                     "language": 1,
#                     "actions_state": 1,
#                     "personality_traits": 1,
#                     "dialouge_style": 1,
#                     "long_term_memory": 1,
#                     "node_based_story": 1,
#                     "knowledge_bank": 1,
#                     "motivation": 1,
#                     "flaws": 1,
#                     "knowledge_filters": 1,
#                     "common_knowledge": 1,
#                     "personal_knowledge": 1,
#                     "safety": 1,
#                     "wikipedia_link": 1,
#                     "safety_status": 1,
#                     "wikipedia_link_status": 1,
#                     "yaml_editor_status": 1,
#                     "scenes": "$attached_scenes"
#                 }
#             }
#         ]

#         characters = list(collection.aggregate(pipeline))
#         if not characters:
#             return {"status": 404, "message": "No characters found."}, 404

#         return characters
#     except Exception as e:
#         return {"status": 500, "message": f"Internal Server Error: {str(e)}"}, 500

# def get_character_image(character_id):
#     try:
#         collection = get_collection()
#         query = {"_id": ObjectId(character_id)}
#         pipeline = [
#             {"$match": query},
#             {
#                 "$project": {
#                     "_id": {"$toString": "$_id"},
#                     "character_id": {"$toString": "$character_id"},
#                     "avatar": {
#                         "$ifNull": [
#                             { "$concat": ["$avatar"] },
#                             None  
#                         ]
#                     }
#                 }
#             }
#         ]

#         cursor = collection.aggregate(pipeline)
#         media = list(cursor)

#         if media:
#             return media[0]  
#         else:
#             return None
#     except Exception as e:
#         logging.error(f"Error in get_story_image: {str(e)}")
#         return None  
    