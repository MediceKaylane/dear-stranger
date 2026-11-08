from models.database import get_connection


def create_comment(post_id, user_id, content):
    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO comments (post_id, user_id, content)
            VALUES (?, ?, ?)
            """,
            (post_id, user_id, content)
        )
        connection.commit()
    finally:
        connection.close()


def get_comments_by_post(post_id):
    connection = get_connection()

    try:
        comments = connection.execute(
            """
            SELECT
                comments.id,
                comments.content,
                comments.created_at,
                users.username
            FROM comments
            JOIN users ON comments.user_id = users.id
            WHERE comments.post_id = ?
            ORDER BY comments.created_at ASC, comments.id ASC
            """,
            (post_id,)
        ).fetchall()

        return comments
    finally:
        connection.close()