from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.comment_model import get_comments_by_post
from services.post_services import publish_post, list_posts, list_user_posts
from flask import abort
from models.user_model import get_user_by_id, get_user_by_username
from models.post_model import get_posts_by_user
from services.comment_services import publish_comment

post_bp = Blueprint("posts", __name__)

@post_bp.route("/feed", methods=["GET", "POST"])
def feed():
    # OpenAI ChatGPT assistance: Connected title submission and draft preservation to the feed.
    title = ""
    content = ""

    if request.method == "POST":

        if "user_id" not in session:
            flash("Please log in to publish.", "error")
            return redirect(url_for("auth.login"))

        content = request.form.get("content")
        title = request.form.get("title", "")

        success, message = publish_post(
            session["user_id"],
            content,
            title
        )

        flash(message, "success" if success else "error")

        if success:
            return redirect(url_for("posts.feed"))

    page = request.args.get("page", 1, type=int)
    page = max(page, 1)

    posts = list_posts(page)

    comments_by_post = {
    post["id"]: get_comments_by_post(post["id"])
        for post in posts
    }


    return render_template(
        "feed.html",
        posts=posts,
        comments_by_post=comments_by_post,
        page=page,
        draft_title=title,
        draft_content=content or ""
    )


@post_bp.route("/profile")
def profile():

    if "user_id" not in session:
        flash("Please log in to view your profile.", "error")
        return redirect(url_for("auth.login"))

    # OpenAI ChatGPT assistance: Look up the username for the signed-in profile.
    user_id = session["user_id"]
    user = get_user_by_id(user_id)
    if user is None:
        session.clear()
        return redirect(url_for("auth.login"))

    posts = list_user_posts(user_id)
    return render_template("profile.html", posts=posts, username=user["username"])

@post_bp.route("/user/<username>")
def public_profile(username):
    user = get_user_by_username(username)

    if user is None:
        abort(404)

    posts = get_posts_by_user(user["id"])

    return render_template(
        "public_profile.html",
        user=user,
        posts=posts
    )

@post_bp.route("/posts/<int:post_id>/reply", methods=["POST"])
def reply(post_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    content = request.form.get("content", "")

    success, message = publish_comment(
        post_id,
        session["user_id"],
        content
    )

    flash(message, "success" if success else "error")

    return redirect(url_for("posts.feed"))
