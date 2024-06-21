from apps import db
from apps.models.users import User
def get_session():
    return db.session

def check_user_exists(query):
    session = get_session()
    user = session.query(User).filter_by(**query).first()
    return user is not None


# def get_user_emails(query, elements):
#     try:
#         collection = get_collection()
#         users = collection.find(query, elements)
#         # emails = [doc["email"] for doc in cursor]
#         return users
#     except Exception as e:
#             return {"status": 301, "message": f"KeyError: {str(e)}"}, 301

# def get_user_detail(query):
#     try:
#         collection = get_collection()
#         collection.create_index({ "email": 1, "is_google_login": 1 })
#         collection.create_index({ "email": 1, "is_microsoft_login": 1 })
#         pipeline = [
#             {"$match":query},
#             {
#                   "$project":{
#                         "_id": { "$toString": "$_id" },
#                         "name":1,
#                         "email":1,
#                         "password":1,
#                         "chat_setting":1,
#                         "is_google_login":1,
#                         "is_microsoft_login":1
#                   }
#             } ]
#         user = collection.aggregate(pipeline)

#         return user
#     except Exception as e:
#             return {"status": 301, "message": f"KeyError: {str(e)}"}, 301

# def get_user_by_id(user_id):
#     try:
#         collection = get_collection()
#         collection.create_index({"email": 1, "is_google_login": 1})

#         pipeline = [
#             {"$match": {"_id": user_id}},
#             {
#                 "$lookup": {
#                     "from": "player",  # Ensure this is the correct collection name
#                     "localField": "_id",
#                     "foreignField": "user_id",
#                     "as": "player_details"
#                 }
#             },
#             {
#                 "$project": {
#                     "_id": {"$toString": "$_id"},
#                     "name": 1,
#                     "email": 1,
#                     "password": 1,
#                     "chat_setting": 1,
#                     "player_details": 1  # Including the player details in the projection
#                 }
#             }
#         ]

#         user = collection.aggregate(pipeline)
#         return list(user)  # Converting the cursor to a list
#     except Exception as e:
#         return {"status": 301, "message": f"KeyError: {str(e)}"}, 301

# def get_user_info(user_id):
#     try:
#         collection = get_collection()
#         collection.create_index({"email": 1, "is_google_login": 1})

#         if isinstance(user_id, str):
#             user_id = ObjectId(user_id)

#         pipeline = [
#             {"$match": {"_id": user_id}},
#             {
#                 "$lookup": {
#                     "from": "player",  
#                     "localField": "_id",
#                     "foreignField": "user_id",
#                     "as": "player_details"
#                 }
#             },
#             {
#                 "$project": {
#                     "_id": {"$toString": "$_id"},
#                     "name": 1,
#                     "email": 1,
#                     "password": 1,
#                     "chat_setting": 1,
#                     "player_details": 1 
#                 }
#             }
#         ]

#         user = list(collection.aggregate(pipeline))

#         if user:
#             return user
#         else:
#             return []  

#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301
   
# def get_collaborator(query, columns):
#     try:
#         collection = get_collection()
#         return collection.find(query, columns)
#     except Exception as e:
#         return {"status": 301, "message": f"KeyError: {str(e)}"}, 301

def add_user(data):
    try:
        session = get_session()
        new_user = User(email=data['email'], password=data['password'], name=data['name'], is_google_login=data['is_google_login'], is_microsoft_login=data['is_microsoft_login'], chat_setting=data['chat_setting'], active=data['active'], deleted=data['deleted'])
        session.add(new_user)
        session.commit()
        return new_user  # Return the id of the newly inserted user
    except Exception as e:
                return {"status": 301, "message": f"KeyError: {str(e)}"}, 301
            
# def update_user_profile(where, data):
#     try:
#         collection = get_collection()
#         return collection.update_one(where, {"$set": data})
#     except Exception as e:
#         print("Error:", e)
#         return False
    
# def update_user_profile_data(user_id, new_hashed_password):
#     try:
#         collection = get_collection()
#         result = collection.update_one(
#             {"_id": ObjectId(user_id)},
#             {"$set": {"password": new_hashed_password}}
#         )
#         return result.modified_count > 0
#     except Exception as e:
#         logging.error(f"Error updating user profile data: {e}")
#         return False

# def delete_user(query):
#     try:
#         collection = get_collection()
#         return collection.find_one_and_delete(query)
#     except Exception as e:
#         return {"status": 301, "message": f"Error: {str(e)}"}, 301
        