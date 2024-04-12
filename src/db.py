from flask import g, current_app
import sqlite3
import click
from werkzeug.security import generate_password_hash

IN_PROGRESS_STATUS = 'В процессе'
DONE_STATUS = 'Выполнено'
ALL_TASKS = 'Все'


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
	try:
		db.execute("DELETE FROM users WHERE id = ?;", (id,))
		db.commit()
		return {'success': True}
	except db.IntegrityError as e:
		return {'success': False, 'error': e}


def delete_task(id):
	db = get_db()
	try:
		db.execute("DELETE FROM tasks WHERE id = ?;", (id,))
		db.commit()
		return {'success': True}
	except db.IntegrityError as e:
		return {'success': False, 'error': e}


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


def get_task_by_id(task_id):
	db = get_db()
	task = db.execute(
				"SELECT * FROM tasks WHERE id = ?;", (task_id,)
		).fetchone()
	return task


def get_filtered_tasks(user_id, filter_status):
	if filter_status != ALL_TASKS:
		db = get_db()
		return db.execute(
				"SELECT * FROM tasks WHERE recipient = ? AND current_status = ?"
				"ORDER BY created DESC;", (user_id, filter_status)
			).fetchall()
	
	return get_user_tasks(user_id)


def get_user_tasks(user_id):
	db = get_db()
	return db.execute(
			"SELECT * FROM tasks WHERE recipient = ? ORDER BY created DESC;", (user_id,)
		).fetchall()


def get_all_users():
	db = get_db()
	return db.execute(
			"SELECT id, first_name, second_name, surname, username, password, is_admin"
			" FROM users;"
		).fetchall()


def get_task_files(id):
	db = get_db()
	files_string = db.execute(
			"SELECT files FROM tasks WHERE id = ?;", (id,)
		).fetchone()
	return files_string["files"].split(";")



def update_task_status(id, status):
	db = get_db()
	if status == "1":
		status = DONE_STATUS
	else:
		status = IN_PROGRESS_STATUS
	try:
		db.execute("UPDATE tasks SET current_status = ? WHERE id = ?;", (status, id))
		db.commit()
	except db.IntegrityError as e:
		return {'success': False, 'error': e}
	return {'success': True}


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
					db.execute(
							"INSERT INTO users"
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


def add_new_task(author_id, recipient, title, body, status, filenames):
	db = get_db()
	error = None
	missing = {author_id: 'автора',
						recipient: 'получатель',
						title: 'заголовок',
						body: 'описание',
						status: 'статус'}

	for i in missing:
		if not i:
			error = f'Укажите {missing[i]} задачи'
			break

	if error is None:
			try:
					db.execute(
							"INSERT INTO tasks"
							"(author_id, recipient, files, title, body, current_status)"
							"VALUES (?, ?, ?, ?, ?, ?)",
							(author_id, recipient, filenames, title, body, status)
						)
					db.commit()
			except db.IntegrityError:
					error = f"Данная задача уже назначена"
			
	if not error is None:
		return {'success': False,
					 'error': error}
	return {'success': True}


def add_default_tasks():
	tasks = [(11, 2, 'task1', 'Lorem Ipsum is simply dummy text of the', IN_PROGRESS_STATUS),
					(11, 2, 'task2', "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard ", IN_PROGRESS_STATUS),
					(12, 3, 'task3', "Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum. Lorem Ipsum is simply dummy text of the printing and typesetting industry.", DONE_STATUS)]
	for task in tasks:
		resp = add_new_task(*task)
		if resp['success']:
			print(f'Added task {task[1]}')
		else:
			print(f"Error while adding task {task[1]}: {resp['error']}")


def add_default_users():
	users = [('admin', 'admin', 'admin', 'admin', 'admin', True),
					('user1', 'user1', 'user1', 'user1', 'user1', False),
					('user2', 'user2', 'user2', 'user2', 'user2', False)]
	for user in users:
		resp = add_new_user(*user)
		if resp['success']:
			print(f"Added new account to database with login '{user[-3]}'")
		else:
			print(f"Error while adding default admin account: {resp['error']}")


def init_db():
	db = get_db()
	with current_app.open_resource("schema.sql") as f:
			db.executescript(f.read().decode("utf8"))


def init_app(app):
	app.teardown_appcontext(close_db)
	app.cli.add_command(init_db_command)
	app.cli.add_command(add_user_command)


@click.command("init-db")
@click.option("--du", default=False)
@click.option("--dt", default=False)
def init_db_command(du, dt):
	init_db()
	if du:
		add_default_users()
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
