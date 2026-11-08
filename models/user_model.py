from models.database import get_connection

def get_user_by_username(username):
    connection = get_connection()

    user = connection.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    ).fetchone()

    connection.close()

    return user

def create_user(username, password_hash):
    connection = get_connection()

    connection.execute(
        "INSERT INTO users (username, password_hash) VALUES (?, ?)",
        (username, password_hash)
    )

    connection.commit()
    connection.close()

def delete_user(user_id):
    connection = get_connection()

    try:
        connection.execute(
            "DELETE FROM posts WHERE user_id = ?",
            (user_id,)
        )

        connection.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )

        connection.commit()
    finally:
        connection.close()