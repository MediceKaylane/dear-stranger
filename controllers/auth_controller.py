from flask import (
    Blueprint, render_template, request,
    redirect, url_for, flash, session
)

from services.auth_services import register_user, authenticate_user, delete_account

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        success, message = register_user(username, password)

        if success:
            flash(message, "success")
            return redirect(url_for("auth.login"))

        flash(message, "error")

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        user = authenticate_user(username, password)

        if user:
            session.clear()
            session["user_id"] = user["id"]

            flash("Welcome back!", "success")
            return redirect(url_for("posts.feed"))

        flash("Invalid username or password.", "error")

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for("index"))

@auth_bp.route("/delete-account", methods=["GET", "POST"])
def delete_account_route():
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        password = request.form.get("password", "")

        success, message = delete_account(
            session["user_id"],
            password
        )

        if success:
            session.clear()
            flash(message, "success")
            return redirect(url_for("index"))

        flash(message, "error")

    return render_template("delete_account.html")