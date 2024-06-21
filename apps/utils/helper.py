import bcrypt
import random
import string
import re

def join_string_by_under_score(input_string):
    lowercase_string = input_string.lower()
    return re.sub(r'\s+', '_', lowercase_string)

def randon_number():
    characters = string.ascii_lowercase  + string.digits
    return ''.join(random.choice(characters) for _ in range(5))

# def hash_password(password):
#     encrypted_password =  bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
#     return encrypted_password

# def verify_password(password, stored_password):
#     return bcrypt.checkpw(password.encode('utf-8'), stored_password)

# Function to hash a password
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to verify a password
def verify_password(provided_password, stored_password):
    # Convert the stored password from hex format to bytes if needed
    if stored_password.startswith('\\x'):
        stored_password = bytes.fromhex(stored_password[2:])

    # Verify the password
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)


def generate_password_hash(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

user_data_store = {}

def store_user_data(user_data):
    email = user_data['email']
    user_data_store[email] = user_data

def retrieve_user_data(email):
    return user_data_store.get(email)