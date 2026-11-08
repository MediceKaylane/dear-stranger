from werkzeug.security import generate_password_hash
from models.user_model import get_user_by_username, create_user
from werkzeug.security import generate_password_hash, check_password_hash

def register_user(username, password):

    if not username or not password:
        return {"error": "Username and password are required."}

    existing_user = get_user_by_username(username)

    if existing_user:
        return False, "Username already exists."

    password_hash = generate_password_hash(password)

    create_user(username, password_hash)
    return True, "User registered successfully."

def authenticate_user(username, password):

    user = get_user_by_username(username)

    if user is None:
        return None

    if not check_password_hash(user["password_hash"], password):
        return None

    return user