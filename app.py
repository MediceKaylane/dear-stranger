import os


from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from controllers.post_controller import post_bp
from controllers.auth_controller import auth_bp
from flask_wtf.csrf import CSRFProtect
from models.database import add_post_titles

# Configure application
app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]

app.register_blueprint(auth_bp)
app.register_blueprint(post_bp)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.environ["SECRET_KEY"]
Session(app)
csrf = CSRFProtect(app)


# OpenAI ChatGPT assistance: Added the command to migrate existing databases.
@app.cli.command("add-post-titles")
def migrate_post_titles():
    """Add a title column to an existing posts table."""
    add_post_titles()


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    if session.get("user_id"):
        return redirect(url_for("posts.feed"))

    return render_template("index.html")
