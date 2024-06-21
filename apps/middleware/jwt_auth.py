from flask import  request, jsonify, g
from flask_jwt_extended import  decode_token
from apps.services.users import *
from bson import ObjectId
# @jwt_bp.before_request
from functools import wraps
from datetime import datetime
from apps.utils.threading_helper import BLACKLIST, remove_from_blacklist

def is_token_expired(decoded_token):
    try:
        expiration_time = datetime.utcfromtimestamp(decoded_token['exp'])
        current_time = datetime.utcnow()
        return current_time > expiration_time
    except Exception as e:
        return jsonify({'error':True, 'status':501, 'message': 'Token has been expired'}), 501

def required_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get('Authorization', '').split('Bearer ')[-1]
        if not access_token:
            return jsonify({"error":301,'error':True, 'message': 'Access token is missing'}), 301
        try:
            decode_access_token = decode_token(access_token)
            if is_token_expired(decode_access_token):
                if decode_access_token['jti'] in BLACKLIST:
                    remove_from_blacklist(decode_access_token['jti'])
                return jsonify({"error":501,'error':True, 'message': 'Token has been expired'}), 501
            try:
                token_jti = decode_access_token['jti']
                if token_jti in BLACKLIST:
                    return jsonify({"error":501,'error': True, 'message': 'User has been deleted'}), 501
                else:
                    g.jti = decode_access_token['jti']
            except Exception as e:
                return jsonify({"error":501,'error': True, 'message': 'User has been deleted'}), 501
        except Exception as e:
                return jsonify({"error":501,'error':True, 'message': 'Token has been expired'}), 501
        g.session_data = decode_access_token['sub']
        return func(*args, **kwargs)
    return wrapper