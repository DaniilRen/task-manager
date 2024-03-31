from flask import url_for, render_template, redirect, flash
from flask import Blueprint, g, session, request
from werkzeug.security import check_password_hash, generate_password_hash
import functools
from db import *

bp = Blueprint('auth', __name__, url_prefix="/auth")


def register():
	if request.method == "POST":
			username = request.form["username"]
			password = request.form["password"]
			db = get_db()
			error = None

			if not username:
					error = "Username is required."
			elif not password:
					error = "Password is required."

			if error is None:
					try:
							db.execute(
									"INSERT INTO user (username, password) VALUES (?, ?)",
									(username, generate_password_hash(password)),
							)
							db.commit()
					except db.IntegrityError:
							# The username was already taken, which caused the
							# commit to fail. Show a validation error.
							error = f"User {username} is already registered."
					else:
							# Success, go to the login page.
							return redirect(url_for("auth.login"))

			flash(error)

	return render_template("auth/register.html")


def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
			if g.user is None:
					return redirect(url_for("auth.login"))

			return view(**kwargs)

	return wrapped_view


@bp.before_app_request
def load_logged_in_user():
	user_id = session.get("user_id")
	g.is_admin = session.get("is_admin")

	if user_id is None:
			g.user = None
	else:
			g.user = (
					get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
			)


@bp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		error = None
		user = get_user(username)

		if user is None:
				error = 'Неверное имя пользователя'
		elif not check_password_hash(user['password'], password):
				error = 'Неверный пароль.'

		if error is None:
				print('Logged in')
				session.clear()
				session['user_id'] = user.id
				if user.is_admin == True:
					session['is_admin'] = True
					return redirect(url_for('admin.admin_panel'))
				return redirect(url_for('index'))
		
		print(f'ERROR: {error}')
		flash(error)

	return render_template('login.html')


@bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))