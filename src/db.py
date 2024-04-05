from flask import g, current_app
import sqlite3
import click
from werkzeug.security import generate_password_hash

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

def delete_user(id):
	db = get_db()
	db.execute(
				"DELETE FROM users WHERE id = ?;", (id,)
		).fetchone()
	return 0

def delete_task(id):
	db = get_db()
	db.execute(
				"DELETE FROM tasks WHERE id = ?;", (id,)
		).fetchone()
	return 0

def get_user_by_name(username):
	db = get_db()
	user = db.execute(
						"SELECT * FROM users WHERE username = ?;", (username,)
				).fetchone()
	return user


def get_user_by_id(user_id):
	db = get_db()
	user = db.execute(
            "SELECT * FROM users WHERE id = ?;", (user_id,)
        ).fetchone()
	return user


def get_all_tasks():
	db = get_db()
	return db.execute(
		"SELECT id, author, title, body, created"
		" FROM tasks ORDER BY created DESC;"
	).fetchall()


def get_all_users():
	db = get_db()
	return db.execute(
		"SELECT id, first_name, second_name, surname, username, password, is_admin"
		" FROM users;"
	).fetchall()


def add_new_user(fstn, secn, surn, login, psw, is_admin):
	db = get_db()
	error = None
	missing = {fstn: 'Имя',
						secn: 'Фамилия',
						surn: 'Отчество',
						login: 'Логин для входа',
						psw: 'Пароль для входа'}

	for i in missing:
		if not i:
			error = f'Укажите {missing[i]}'
			break

	if error is None:
			try:
					hashed_psw = generate_password_hash(psw)
					db.execute("INSERT INTO users"
						"(first_name, second_name, surname, username, password, is_admin)"
						"VALUES (?, ?, ?, ?, ?, ?);",
						(fstn, secn, surn, login, hashed_psw, is_admin)
						)
					db.commit()
			except db.IntegrityError:
					error = f"Имя пользователя '{login}' уже занято"
			
	if not error is None:
		return {'success': False,
					 'error': error}
	return {'success': True}


def add_default_admin():
	resp = add_new_user('admin', 'admin', 'admin', 'admin', 'admin', True)
	if resp['success']:
		print('Added default admin account')
	else:
		print(f"Error while adding default admin account: {resp['error']}")


def add_new_task(author, title, body):
	db = get_db()
	error = None
	missing = {author: 'автора',
						title: 'заголовок',
						body: 'описание'}

	for i in missing:
		if not i:
			error = f'Укажите {missing[i]} задачи'
			break

	if error is None:
			try:
					db.execute("INSERT INTO tasks"
						"(author, title, body)"
						"VALUES (?, ?, ?)",
						(author, title, body)
						)
					db.commit()
			except db.IntegrityError:
					error = f"Данная задача уже назначена"
			
	if not error is None:
		return {'success': False,
					 'error': error}
	return {'success': True}


def add_default_tasks():
	tasks = [('daniil', 'task1', 'body1'), ('daniil', 'task2', 'body2'*20), ('daniil', 'task3', 'body3')]
	for task in tasks:
		resp = add_new_task(*task)
		if resp['success']:
			print(f'Added task {task[1]}')
		else:
			print(f"Error while adding task {task[1]}: {resp['error']}")


def init_db():
	db = get_db()
	with current_app.open_resource("schema.sql") as f:
			db.executescript(f.read().decode("utf8"))


def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
	app.cli.add_command(add_user_command)


@click.command("init-db")
@click.option("--da", default=False)
@click.option("--dt", default=False)
def init_db_command(da, dt):
	init_db()
	if da:
		add_default_admin()
	if dt:
		add_default_tasks()
	click.echo("Initialized the database.")


@click.command("add-user")
@click.option("--fstn", required=True, type=str)
@click.option("--secn", required=True, type=str)
@click.option("--surn", required=True, type=str)
@click.option("--login", required=True, type=str)
@click.option("--psw", required=True, type=str)
@click.option("--isadm", required=True, type=bool)
def add_user_command(fstn, secn, surn, login, psw, isadm):
	resp = add_new_user(fstn, secn, surn, login, psw, isadm)
	if resp['success'] == True:
		click.echo(f"Added new account to database with login '{login}'")
	else:
		click.echo(resp['error'])
