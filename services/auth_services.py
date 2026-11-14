from werkzeug.security import generate_password_hash
from models.user_model import get_user_by_username, create_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.security import check_password_hash
from models.user_model import delete_user
from models.database import get_connection

def register_user(username, password):

    if not username or not password:
        # OpenAI ChatGPT assistance: Return the result pair expected by the controller.
        return False, "Username and password are required."

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

def delete_account(user_id, password):
    connection = get_connection()

    try:
        user = connection.execute(
            "SELECT password_hash FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
    finally:
        connection.close()

    if user is None:
        return False, "User not found."

    if not check_password_hash(user["password_hash"], password):
        return False, "Incorrect password."

    delete_user(user_id)

    return True, "Your account has been deleted."
