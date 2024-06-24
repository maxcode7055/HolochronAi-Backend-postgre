from flask import Blueprint, request, jsonify, g, current_app,  render_template #redirect, url_for
# from apps.middleware.jwt_auth import required_token
from apps.utils.helper import *
from apps.services.users import check_user_exists, add_user,  get_user_detail, create_user_filter #, update_user_profile, get_user_info, update_user_profile_data
from flask_jwt_extended import create_access_token, decode_token
# from apps.routes.character import create_default_character
from apps.routes.workspace import create_default_workspace
from apps.routes.users import add


from apps.services.user_workspaces_services import *
import requests
from apps.tasks import send_email
from datetime import timedelta
import logging
# from line_profiler import profile

auth_bp = Blueprint('auth', __name__)
class AuthService:

    @auth_bp.route('/login', methods=['POST'])
    def login():
        try:
            data = request.json
            email = data.get('email', '').lower()
            password = data.get('password')
            if not email or not password:
                return jsonify({'status': 400, 'error': True, 'message': 'Email and password are required'}), 400
            user_query = create_user_filter(email)
            user = get_user_detail(user_query)
            if not user:
                return jsonify({'status': 301, 'error': True, 'message': 'No such user existed.'}), 301
            if verify_password(password, user.password):
                expires = timedelta(hours=24)
                token = create_access_token(identity={
                    'name': user.name,
                    'email': user.email.lower(),
                    'id': str(user.id)
                }, expires_delta=expires)

                userdata = {
                    "has_password": True,
                    "_id": str(user.id),
                    'name': user.name,
                    'email': user.email.lower()
                }
                return jsonify({
                    'status': 200,
                    'error': False,
                    'message': 'Login successful',
                    'data': {'userdata': userdata, "access_token": token}
                }), 200
            else:
                return jsonify({'status': 301, 'error': True, 'message': 'Invalid email or password'}), 301

        except KeyError as e:
            return jsonify({'status': 400, 'error': True, 'message': f"KeyError: {str(e)}"}), 400
        except Exception as e:
            print(e)
            return jsonify({'status': 500, 'error': True, 'message': 'An unexpected error occurred'}), 500  
      
    # @auth_bp.route('/logout', methods=['POST'])
    # def logout():
    #     # Logout logic
    #     pass

    @auth_bp.route('/checkemail', methods=['POST'])
    def checkemail():
        try:
            email = request.json.get('email')
            
            user_exists = check_user_exists({"email":email.lower()})
            if user_exists:
                return jsonify({'status':301,'error': True,'message': f"User '{email.lower()}' exists"}), 301
            else:
                return jsonify({'status':200,'error': False,'message': 'User not existed.'}), 200
        except Exception as e:
            return jsonify({'status':301,'error': True, "message": f"KeyError: {str(e)}"}), 301


    @auth_bp.route('/register', methods=['POST'])
    def register():
        try:
            email = request.json.get('email')
            password = request.json.get('password')
            name = request.json.get('fullname')
            user_exists = check_user_exists({"email": email.lower()})

            if user_exists:
                return jsonify({'status': 301, 'error': True, 'message': f"User '{email.lower()}' exists"}), 301
            
            user_data = {
                'email': email.lower(),
                'password': password,
                'name': name
            }
            # Store the user data in a temporary storage or database
            store_user_data(user_data)
            expires = timedelta(hours=24)
            token = create_access_token(identity=user_data, expires_delta=expires)
            verification_link = f"{current_app.config['DEVELOPMENT_FRONT_URL']}/verifyemail?token={token}"
            
            html_content = render_template('verify_email.html', verification_link=verification_link)
            send_email("Verify email id", email.lower(), html_content)
            return jsonify({'status': 200, 'error': False, 'message': f"A verification link has been sent to email id {email.lower()}.", 'verification_link': verification_link}), 200
        
        except Exception as e:
            return jsonify({'status': 301, 'error': True, 'message': 'General error: ' + str(e)}), 301


    # @auth_bp.route('/reverification', methods=['POST'])
    # def reverification():
    #     try:
    #         email = request.json.get('email')
    #         if not email:
    #             return jsonify({'status': 400, 'error': True, 'message': 'Email is required'}), 400
            
    #         user_exists = check_user_exists({"email": email.lower()})
    #         if user_exists:
    #             return jsonify({'status': 400, 'error': True, 'message': f"User '{email.lower()}' is already registered"}), 400
            
    #         # Retrieve the user data stored during registration
    #         user_data = retrieve_user_data(email.lower())
    #         if not user_data:
    #             return jsonify({'status': 404, 'error': True, 'message': f"User data not found for '{email.lower()}'"}), 404
            
    #         expires = timedelta(hours=24)
    #         token = create_access_token(identity=user_data, expires_delta=expires)
    #         verification_link = f"{current_app.config['DEVELOPMENT_FRONT_URL']}/verifyemail?token={token}"
            
    #         html_content = render_template('verify_email.html', verification_link=verification_link)
    #         send_email("Verify your email", email.lower(), html_content)
            
    #         return jsonify({'status': 200, 'error': False, 'message': f"A Reverification link has been sent to {email.lower()}.", 'verification_link': verification_link}), 200
        
    #     except Exception as e:
    #         return jsonify({'status': 500, 'error': True, 'message': f"General error: {str(e)}"}), 500

    
    @auth_bp.route('/verifyemail', methods=['GET'])
    def verify_email():
        try:
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return jsonify({"error":True,"status": 301, "message": "Authorization header is missing"}), 301
            token = auth_header.split(" ")[1]  # Extract token from header
            decoded_token = decode_token(token)
            if decoded_token:
                user_exists = check_user_exists({"email": decoded_token['sub']['email'].lower()})
                if user_exists:
                    return jsonify({'status': 301, 'error': True, 'message': f"User '{decoded_token['sub']['email'].lower()}' exists"}), 301
                added_user_id = add(decoded_token['sub'])
                if added_user_id:
                    workspace_id = create_default_workspace()
                    user_workspace_data = {
                        'user_id': added_user_id,
                        'workspace_id': workspace_id,
                        'deleted':False,
                        'active':True
                    }
                    d = user_workspaces_add(user_workspace_data)
                    expires = timedelta(hours=24)
                    token = create_access_token(identity={'name':decoded_token['sub']['name'],'email':decoded_token['sub']['email'].lower(),"id":str(added_user_id)}, expires_delta=expires)
                    return jsonify({ 'status':200,'error': False, 'message': 'User has been verified successfully.', 'data':{"_id":str(added_user_id),'userdata':{
                        'name':decoded_token['sub']['name'],
                        'email':decoded_token['sub']['email'].lower(),
                        "has_password":True
                        }, "access_token":token}}), 200
                else:
                    return jsonify({'status':301, 'error': True, 'message': 'Unable to verify user right now.'}), 301
            else:
                return jsonify({'status':301, 'error': True, 'message': 'Token has been expired c.'}), 301
        except Exception as e:
            return jsonify({'status':301, 'error': True, "message": "Token has been expired."}), 301

    
    
    
    # @auth_bp.route('/accept-invite', methods=['GET'])
    # def accept_invite():
    #     try:
    #         # auth_header = request.headers.get('Authorization')

    #         token = request.args.get('token')
    #         if not token:
    #             return jsonify({"error":True,"status": 301, "message": "Token is missing"}), 301
    #         decoded_token = decode_token(token)
            
            
    #         user_exists = list(get_user_detail({"_id":ObjectId(decoded_token['sub']['_id']), "active":True}))
    #         if user_exists:
    #             return jsonify({"error":True,"status": 301, "message": "Token has been expired"}), 301
    #         datatobeupdate = {"active":True}
    #         datatobeupdate['password'] =  hash_password(randon_number())
            
    #         if decoded_token:
    #             # added = update_user_profile({decoded_token['sub']})
    #             updated = update_user_profile({"_id":ObjectId(decoded_token['sub']['_id'])}, datatobeupdate )
                
    #             if updated.acknowledged:
                    
    #                 workspace_id = create_default_workspace()
                   
    #                 user_workspace_data = {
    #                     'user_id': ObjectId(decoded_token['sub']['_id']),
    #                     'workspace_id': ObjectId(workspace_id),
    #                     'deleted':False,
    #                     'active':True
    #                 }
    #                 user_workspaces_add(user_workspace_data)
    #                 expires = timedelta(hours=24)
    #                 token = create_access_token(identity={'name':decoded_token['sub']['email'].lower(),'email':decoded_token['sub']['email'].lower(),"id":str(decoded_token['sub']['_id'])}, expires_delta=expires)
                    
    #                 return jsonify({ 'status':200,'error': False, 'message': 'User invite has been accepted successfully.', 'data':{
    #                     "_id":str(decoded_token['sub']['_id']),'userdata':{
    #                         'name':decoded_token['sub']['email'].lower(),
    #                         'email':decoded_token['sub']['email'].lower(), 
    #                         "has_password":False}, "access_token":token}}), 200
    #             else:
    #                 return jsonify({'status':301, 'error': True, 'message': 'Unable to verify user right now.'}), 301
    #         else:
    #             return jsonify({'status':301, 'error': True, 'message': 'Token has been expired ccc.'}), 301
    #     except Exception as e:
    #         return jsonify({'status':301, 'error': True, "message": "Token has been expired s."}), 301

    # @auth_bp.route('/signup-with-google', methods=['POST'])
    # def signup_with_google():
    #     try:
    #         data = request.get_json()
    #         auth_code = data['code']
    #         redirect_uri = data['redirect_uri']
    #         response = requests.post('https://oauth2.googleapis.com/token', data={
    #             'code': auth_code,
    #             'client_id': current_app.config['GOOGLE_API_KEY'],
    #             'client_secret': current_app.config['GOOGLE_SECRET_KEY'],
    #             'redirect_uri': redirect_uri,
    #             'grant_type': 'authorization_code'
    #         })
    #         if response.status_code == 200:
    #             access_token = response.json().get('access_token')
    #         else:
    #             response_dataone = {
    #                 "status": 400,
    #                 "message": "Failed to obtain access token. Please check code",
    #                 "data": {}
    #             }
    #             return response_dataone, 400
    #         if access_token:
    #             access_token = access_token
    #             person_data_url = "https://people.googleapis.com/v1/people/me?personFields=names,emailAddresses"
    #             person_data_response = requests.get(person_data_url, headers={
    #                 "Authorization": f"Bearer {access_token}"
    #             })
    #             if person_data_response.status_code == 200:
    #                 person_data = person_data_response.json()
    #                 # Do whatever you want with person_data
    #                 given_name = ""
    #                 family_name =""
    #                 email = ""
                    
    #                 if 'names' in person_data and len(person_data['names']) > 0:
    #                     given_name = person_data['names'][0].get(
    #                         'givenName', '')
    #                     family_name = person_data['names'][0].get(
    #                         'familyName', '')
    #                     name =f"{given_name.lower()} {family_name.lower()}"

    #                 # Extract email address
    #                 if 'emailAddresses' in person_data and len(person_data['emailAddresses']) > 0:
    #                     email = person_data['emailAddresses'][0].get( 'value', '')

    #                 user_data = {
    #                     'email': email.lower(),
    #                     'password': "",
    #                     'name': f"{given_name.lower()} {family_name.lower()}",
    #                     "is_google_login":True,
    #                     "chat_setting":25
    #                 }
    #                 user_exists = list(get_user_detail({"email":email.lower()}))
    #                 if user_exists and len(user_exists):
    #                     expires = timedelta(hours=24)
    #                     token = create_access_token(identity={'name':user_data['name'],'email':user_data['email'].lower(),"id":str(user_exists[0]['_id'])}, expires_delta=expires)
    #                     return jsonify({ 'status':200,'error': False, 'message': 'User has been verified successfully.', 'data':{'userdata':{"has_password":True, "_id":str(user_exists[0]['_id']),'name':user_data['name'],'email':user_data['email'].lower()}, "access_token":token}}), 200
    #                 else:
    #                     added = add(user_data)
    #                     #workspace and characters should be added here
    #                     if added:
    #                         workspace_id = create_default_workspace()
                   
    #                         user_workspace_data = {
    #                             'user_id': added,
    #                             'workspace_id': ObjectId(workspace_id),
    #                             'deleted':False,
    #                             'active':True
    #                         }
    #                         user_workspaces_add(user_workspace_data)
    #                         expires = timedelta(hours=24)
    #                         token = create_access_token(identity={'name':user_data['name'],'email':user_data['email'].lower(),"id":str(added)}, expires_delta=expires)
    #                         return jsonify({ 'status':200,'error': False, 'message': 'User has been verified successfully.', 'data':{'userdata':{"has_password":True, "_id":str(added),'name':user_data['name'],'email':user_data['email'].lower()}, "access_token":token}}), 200
    #                     else:
    #                         return jsonify({'status':301, 'error': True, 'message': 'Unable to verify user right now.'}), 301
    #             else:
    #                 return { "status": 301, "error":True, "message": "Error processing token", "data": {}}, 301

    #         else:
    #             return {"status": 301, "error":True, "message": "NO Access Token Found","data": {} }, 301

    #     except Exception as e:
    #         return {"status": 301,"error":True, "message": f"KeyError: {str(e)}"}, 301
              
    # @auth_bp.route('/signup-with-microsoft', methods=['POST'])
    # def signup_with_microsoft():
    #     try:
    #         data = request.get_json()
    #         if not "username" in data:
    #             return {"status": 301, "error":True, "message": "Please sned username","data": {} }, 301
    #         user_data = {
    #             'email': data['username'],
    #             'password': "",
    #             'name': data['name'],
    #             "is_microsoft_login":True,
    #             "is_google_login":False,
    #             "chat_setting":25
    #         }
    #         user_exists = list(get_user_detail({"email":data['username'].lower()}))
            
    #         if user_exists and len(user_exists):
    #             if "is_google_login" in user_exists[0] and "is_microsoft_login" not in user_exists[0]:
    #                 return {"status": 301, "error":True, "message": "This user is not available, please try login via another user.","data": {} }, 301
    #             if "is_google_login" not in user_exists[0] and "is_microsoft_login" not in user_exists[0]:
    #                 return {"status": 301, "error":True, "message": "This user is not available, please try login via another user.","data": {} }, 301
                
    #             expires = timedelta(hours=24)
    #             token = create_access_token(identity={'name':user_data['name'],'email':user_data['email'].lower(),"id":str(user_exists[0]['_id'])}, expires_delta=expires)
    #             return jsonify({ 'status':200,'error': False, 'message': 'User has been verified successfully.', 'data':{'userdata':{"has_password":True, "_id":str(user_exists[0]['_id']),'name':user_data['name'],'email':user_data['email'].lower()}, "access_token":token}}), 200
    #         else:
    #             added = add(user_data)
    #             if added:
    #                 workspace_id = create_default_workspace()
            
    #                 user_workspace_data = {
    #                     'user_id': added,
    #                     'workspace_id': ObjectId(workspace_id),
    #                     'deleted':False,
    #                     "is_microsoft_login":True,
    #                     "is_google_login":False,
    #                     'active':True
    #                 }
    #                 user_workspaces_add(user_workspace_data)
    #                 expires = timedelta(hours=24)
    #                 token = create_access_token(identity={'name':user_data['name'],'email':user_data['email'].lower(),"id":str(added)}, expires_delta=expires)
    #                 return jsonify({ 'status':200,'error': False, 'message': 'User has been verified successfully.', 'data':{'userdata':{"has_password":True, "_id":str(added),'name':user_data['name'],'email':user_data['email'].lower()}, "access_token":token}}), 200
    #             else:
    #                 return jsonify({'status':301, 'error': True, 'message': 'Unable to verify user right now.'}), 301
    #     except Exception as e:
    #         return {"status": 301,"error":True, "message": f"KeyError: {str(e)}"}, 301
   
   
    # @auth_bp.route('/api/forget-password-request', methods=['POST'])
    
    # def forget_password_request():
    #     try:
    #         data = request.get_json()
    #         if not "email" in data:
    #             return {"status": 301, "error":True, "message": "Please sned your email id","data": {} }, 301
            
    #         user_exists = check_user_exists({"email":data["email"].lower(), "is_google_login":False,  "deleted":False})
    #         if user_exists:
    #             verification_link = f"{current_app.config['DEVELOPMENT_FRONT_URL']}/api/save-password?token={create_access_token(identity={'email':data['email'].lower()}, expires_delta=timedelta(hours=2))}"
    #             html_content = render_template('save_password_mail.html',  verification_link=verification_link)
    #             send_email("Verify email id", data["email"].lower(), html_content)
    #             return jsonify({'status':200, 'error': False, 'message': f"A verification link has been sent to email id {data['email'].lower()}.", 'verification_link':verification_link}), 200
    #         else:
    #             return jsonify({'status':200,'error': False,'message': 'User not existed.'}), 200
            
    #     except Exception as e:
    #         return {"status": 301,"error":True, "message": f"KeyError: {str(e)}"}, 301
        
    # @auth_bp.route('/api/save-password', methods=['POST'])    
    # def save_password():
    #     try:
    #         data = request.get_json()
            
    #         if not "password" in data:
    #             return jsonify({"status": 301, "error":True, "message": "Please enter new password","data": {} }), 301
            
    #         token = request.args.get('token')
    #         if not token:
    #             return jsonify({"error":True,"status": 301, "message": "Token is missing"}), 301
    #         decoded_token = decode_token(token)
            
    #         user_exists = check_user_exists({"email":decoded_token['sub']['email'], "active":True, "is_google_login":False,  "deleted":False})
    #         if not user_exists:
    #             return jsonify({"error":True,"status": 301, "message": "No such user exists."}), 301
            
    #         datatobeupdate = {'password' :  hash_password(data['password'])}
    #         updated = update_user_profile({"email":decoded_token['sub']['email']}, datatobeupdate )
            
    #         if updated.acknowledged:
    #             return jsonify({"status": 200, "error":False, "message": "Your password has been changed successfully.","data": {} }), 200
    #         return jsonify({"status": 301, "error":True, "message": "This action can not be perform right now.","data": {} }), 301
    #     except Exception as e:
    #         return {"status": 301,"error":True, "message": f"KeyError: {str(e)}"}, 301


    # @auth_bp.route('/api/change-password', methods=['POST'])
    # @required_token
    # def change_password():
    #     try:
    #         session_data = getattr(g, 'session_data', None)

    #         if not session_data or 'id' not in session_data:
    #             return jsonify({'status': 301, 'error': True, 'message': 'User session data missing', 'data': []}), 301

    #         user_id = session_data['id']
    #         logging.info(f"User ID from session: {user_id}")

    #         data = request.get_json()
            
    #         if not ("old_password" in data and "new_password" in data):
    #             return jsonify({"status": 400, "error": True, "message": "Both old_password and new_password are required."}), 400
            
    #         user_details = get_user_info(user_id)
            
    #         if user_details:
    #             user_data = user_details[0]
    #             stored_hashed_password = user_data.get("password")
    #         else:
    #             return jsonify({"status": 404, "error": True, "message": "User not found."}), 404
            
    #         old_password = data['old_password']
            
    #         if not verify_password(old_password, stored_hashed_password):
    #             return jsonify({"error": True, "status": 401, "message": "Invalid old password."}), 401
            
    #         new_hashed_password = generate_password_hash(data['new_password'])
    #         updated = update_user_profile_data(user_id, new_hashed_password)
            
    #         if updated:
    #             return jsonify({"status": 200, "error": False, "message": "Your password has been changed successfully."}), 200
    #         else:
    #             return jsonify({"status": 500, "error": True, "message": "Failed to update password."}), 500
    #     except Exception as e:
    #         logging.error(f"Internal Server Error: {e}")
    #         return jsonify({"status": 500, "error": True, "message": f"Internal Server Error: {str(e)}"}), 500
