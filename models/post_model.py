from models.database import get_connection

def create_post(user_id, content):
    connection = get_connection()

    connection.execute(
        "INSERT INTO posts (user_id, content) VALUES (?, ?)",
        (user_id, content)
    )

    connection.commit()
    connection.close()

def get_posts_by_user(user_id):
    connection = get_connection()

    posts = connection.execute(
        """
        SELECT id, content, created_at
        FROM posts
        WHERE user_id = ?
        ORDER BY created_at DESC, id DESC
        """,
        (user_id,)
    ).fetchall()

    connection.close()

    return posts

def get_all_posts(page=1):
    connection = get_connection()

    limit = 5
    offset = (page - 1) * limit

    posts = connection.execute("""
    SELECT
        posts.id,
        posts.content,
        posts.created_at,
        users.username
    FROM posts
    JOIN users ON posts.user_id = users.id
    ORDER BY posts.created_at DESC, posts.id DESC
    LIMIT ? OFFSET ?
""", (limit, offset)).fetchall()

    connection.close()
    return posts