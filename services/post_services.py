from models.post_model import create_post, get_all_posts, get_posts_by_user

def publish_post(user_id, content):

    if not content or not content.strip():
        return False, "Your post cannot be empty."

    if len(content) > 2000:
        return False, "Your post is too long."

    create_post(user_id, content.strip())

    return True, "Your story has been published."

def list_posts(page=1):
    return get_all_posts(page)

def list_user_posts(user_id):
    return get_posts_by_user(user_id)