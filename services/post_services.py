from models.post_model import create_post, get_all_posts, get_posts_by_user

# OpenAI ChatGPT assistance: Added title validation before saving a new story.
def publish_post(user_id, content, title):
    title = (title or "").strip()
    if not title:
        return False, "Please give your story a title."

    if len(title) > 100:
        return False, "Your title cannot exceed 100 characters."

    if not content or not content.strip():
        return False, "Your post cannot be empty."

    if len(content) > 2000:
        return False, "Your post is too long."

    create_post(user_id, content.strip(), title)

    return True, "Your story has been published."

def list_posts(page=1):
    return get_all_posts(page)

def list_user_posts(user_id):
    return get_posts_by_user(user_id)
