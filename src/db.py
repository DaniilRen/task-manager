from flask import g, current_app
import sqlite3


def get_db():
	if "db" not in g:
			g.db = sqlite3.connect(
					current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
			)
			g.db.row_factory = sqlite3.Row
	return g.db


def close_db(e=None):
	db = g.pop("db", None)
	if db is not None:
			db.close()


def init_db():
	db = get_db()

	with current_app.open_resource("schema.sql") as f:
		db.executescript(f.read().decode("utf8"))


def init_app(app):
	app.teardown_appcontext(close_db)


def get_user(username):
	db = get_db()
	user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()
	return user


def get_all_users():
	db = get_db()
	users = db.execute(
		"SELECT p.id, title, body, created, author_id, username"
		" FROM post p JOIN user u ON p.author_id = u.id"
		" ORDER BY created DESC"
	).fetchall()
	return users