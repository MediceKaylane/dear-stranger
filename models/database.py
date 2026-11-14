import sqlite3
from contextlib import closing

DATABASE = "dearstranger.db"

def get_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# OpenAI ChatGPT assistance: Added this migration to preserve old posts without titles.
def add_post_titles():
    with closing(get_connection()) as connection, connection:
        # Lock writes while checking and updating the schema.
        connection.execute("BEGIN IMMEDIATE")
        columns = connection.execute("PRAGMA table_info(posts)").fetchall()
        if columns and all(column["name"] != "title" for column in columns):
            connection.execute("ALTER TABLE posts ADD COLUMN title TEXT")
