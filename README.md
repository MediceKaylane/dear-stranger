# Dear Stranger

**Video Demo:** https://www.youtube.com/watch?v=qQRnlJqClZs

## Description

Dear Stranger is a web application where people can share thoughts, feelings, and personal experiences under a chosen username. I wanted to give people a place to write about an experience, read what someone else had shared, and respond. The name reflects the idea of writing to someone you may never meet. A username lets readers recognize a writer across stories without requiring a real name.

Visitors can browse the feed and open public profiles. Registered users can sign in, publish titled stories, and reply to posts. The feed displays five stories per page with replies grouped under the original story. My Profile shows the signed-in user's username and stories. The account deletion form asks for password confirmation before the account and its posts are removed. Related replies are removed through SQLite foreign keys.

New stories require a title of up to 100 characters and a body of up to 2,000 characters. Replies can be up to 500 characters. These rules are checked on the server. Stories created before titles were introduced still appear in the feed and profiles. The application stores password hashes using Werkzeug, manages sessions with Flask-Session, and checks form tokens with Flask-WTF.

## Architecture and files

I organized the project around Model–View–Controller with a service layer for validation. A story submission starts in the feed controller, which reads the title and body. The post service validates both fields before calling the model to save them. The feed then uses a Jinja template to display the updated list.

- `app.py` configures Flask, sessions, and CSRF protection. It registers the route groups, defines the homepage, and provides the command to update an older database.
- `controllers/auth_controller.py` handles registration, login, logout, and account deletion. `controllers/post_controller.py` handles the feed, publishing, profiles, and replies.
- `models/database.py` opens SQLite connections, enables foreign key checks, and adds the title column to existing databases. `models/user_model.py` reads, creates, and deletes accounts. `models/post_model.py` saves stories and retrieves them for the feed and profiles. `models/comment_model.py` inserts replies and retrieves them by post.
- `services/auth_services.py` checks credentials and handles registration and password confirmation. `services/post_services.py` and `services/comment_services.py` validate stories and replies before the models save them.
- `schema.sql` defines the users, posts, and comments tables. `requirements.txt` lists the packages needed to run the application. `.gitignore` excludes local environments, secrets, session files, and databases from version control.

In `templates/`, `layout.html` provides the shared navigation and page structure. `index.html` introduces the site and displays the illustration. `login.html`, `register.html`, and `delete_account.html` provide the account forms. `feed.html` combines the story form, story cards, replies, and navigation between pages. `profile.html` shows the signed-in user's stories and `public_profile.html` shows stories by the requested username. The root-level `dearstranger.html` is an earlier layout draft.

The interface uses Bootstrap with custom rules in `static/css/style.css`. The favicon, duck animation, and homepage illustration are kept in `static/images/`.

## Design choices and challenges

My biggest challenge was deciding how to structure the application and in what order to build its parts. A reply needs both an existing user and an existing post. A profile needs a way to retrieve stories by author. Account deletion requires deciding what happens to all the records that refer to that account. Working through these dependencies helped me plan the project and understand how the database affects the behavior users see.

The MVC structure helped me decide where new code belonged. Keeping queries in models means I can see what the program does with data without reading the HTML. The service layer gives validation a consistent place and lets route code focus on handling the request. SQLite let me work directly with SQL and foreign keys using a single database file. Bootstrap gave me a starting point for forms and cards, and I used custom colors and illustrations to give the site its own appearance.

## Running locally

From the project directory, create and activate a Python virtual environment. Install dependencies with `python -m pip install -r requirements.txt` and set the `SECRET_KEY` environment variable to a private random value. To create a new SQLite database, run:

```sh
python -c "import sqlite3; from pathlib import Path; db = sqlite3.connect('dearstranger.db'); db.executescript(Path('schema.sql').read_text(encoding='utf-8-sig')); db.close()"
```

If your database predates story titles, run `python -m flask --app app add-post-titles`. Start the site with `python -m flask --app app run` and open the local address printed by Flask.

## Future improvements

I would like to review and strengthen application security, add private chat, let users report inappropriate posts, and add likes to stories.

## AI assistance

I used OpenAI ChatGPT to draft much of the HTML and to help with the homepage illustration, title handling, profile username display, troubleshooting, and documentation. Comments in the relevant source files identify the assistance.
