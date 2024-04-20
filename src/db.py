from flask import g, current_app
import sqlite3
import click
from werkzeug.security import generate_password_hash

IN_PROGRESS_STATUS = 'В процессе'
DONE_STATUS = 'Выполнено'
ALL_TASKS = 'Все'


""" Перевод численного статуса в буквенный  """
def convert_task_status(status: str) -> str:
	if status == "0": 
		return IN_PROGRESS_STATUS
	elif status == "1":
		return DONE_STATUS
	else: 
		return ALL_TASKS


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
		return {'status': 'success'}
	except db.IntegrityError as e:
		return {'status': e}


def delete_task(id):
	db = get_db()
	try:
		db.execute("DELETE FROM tasks WHERE id = ?;", (id,))
		db.commit()
	except db.IntegrityError as e:
		return {'status': e}
	return {'status': 'success'}


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


def get_all_users(current_user_id):
	db = get_db()
	return db.execute(
			"SELECT id, first_name, second_name, surname, username, password, is_admin"
			" FROM users WHERE id != ?;", (current_user_id,)
		).fetchall()


def get_task_files(id):
	db = get_db()
	files_string = db.execute(
			"SELECT files FROM tasks WHERE id = ?;", (id,)
		).fetchone()
	return [file for file in files_string["files"].split(";") if file != ""]


def update_task_files(id, new_filenames):
	db = get_db()
	old_files = get_task_files(id)
	if len(old_files) == 1:
		filenames = new_filenames
	else: 
		filenames = ";".join(old_files) + ";" + new_filenames
	print(f"Updating task {id} files to {filenames}")
	try:
		db.execute("UPDATE tasks SET files = ? WHERE id = ?;", (filenames, id))
		db.commit()
	except db.IntegrityError as e:
		return {'status': e}
	return {'status': 'success'}


def update_task_status(id, status):
	db = get_db()
	try:
		db.execute("UPDATE tasks SET current_status = ? WHERE id = ?;", (status, id))
		db.commit()
	except db.IntegrityError as e:
		return {'status': e}
	return {'status': 'success'}


def update_task_deadline(id, deadline):
	db = get_db()
	try:
		db.execute("UPDATE tasks SET deadline = ? WHERE id = ?;", (deadline, id))
		db.commit()
	except db.IntegrityError as e:
		return {'status': e}
	return {'status': 'success'}


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
		return {'status': error}
	return {'status': 'success'}


def add_new_task(author_id, recipient, title, body, status, deadline=" ", filenames=";"):
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
							"(author_id, recipient, files, title, body, current_status, deadline)"
							"VALUES (?, ?, ?, ?, ?, ?, ?)",
							(author_id, recipient, filenames, title, body, status, deadline)
						)
					db.commit()
			except db.IntegrityError:
					error = f"Данная задача уже назначена"
			
	if not error is None:
		return {'status': error}
	return {'status': 'success'}


def add_default_tasks():
	tasks = [(1, 2, 'Задача 1', 'Описание в приложенном файле', IN_PROGRESS_STATUS, "До 7.08.2024"),
					(1, 2, 'Задача 2', "Описание в приложенном файле", IN_PROGRESS_STATUS, "До 13.05.2025")]
	for task in tasks:
		resp = add_new_task(*task)
		if resp['status'] == "success":
			print(f"Added task '{task[2]}'")
		else:
			print(f"Error while adding task {task[1]}: {resp['status']}")


def add_default_users():
	users = [('Perviy Med Pavlova', '-', '-', 'PerviyMedPavlova', 'PerviyMedPavlova', True),
					('Litera V', '-', '-', 'LiteraV', 'LiteraV', False)]
	for user in users:
		resp = add_new_user(*user)
		if resp['status'] == "success":
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
	if resp['status'] == "success":
		click.echo(f"Added new account to database with login '{login}'")
	else:
		click.echo(resp['error'])
