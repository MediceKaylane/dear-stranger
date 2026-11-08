from models.comment_model import create_comment


def publish_comment(post_id, user_id, content):
    content = (content or "").strip()

    if not content:
        return False, "Reply cannot be empty."

    if len(content) > 500:
        return False, "Reply must be 500 characters or less."

    create_comment(post_id, user_id, content)

    return True, "Reply published successfully."