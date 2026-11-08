from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.post_services import publish_post, list_posts, list_user_posts
from flask import abort
from models.user_model import get_user_by_username
from models.post_model import get_posts_by_user

post_bp = Blueprint("posts", __name__)

@post_bp.route("/feed", methods=["GET", "POST"])
def feed():

    if request.method == "POST":

        if "user_id" not in session:
            flash("Please log in to publish.", "error")
            return redirect(url_for("auth.login"))

        content = request.form.get("content")

        success, message = publish_post(
            session["user_id"],
            content
        )

        flash(message, "success" if success else "error")

        if success:
            return redirect(url_for("posts.feed"))

    page = request.args.get("page", 1, type=int)
    page = max(page, 1)

    posts = list_posts(page)

    return render_template(
        "feed.html",
        posts=posts,
        page=page
    )


@post_bp.route("/profile")
def profile():

    if "user_id" not in session:
        flash("Please log in to view your profile.", "error")
        return redirect(url_for("auth.login"))

    posts = list_user_posts(session["user_id"])

    return render_template("profile.html", posts=posts)

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