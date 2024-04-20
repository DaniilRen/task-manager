from flask import render_template, g, Blueprint, request, url_for, redirect, flash, session, current_app, send_from_directory, abort
from . import auth, db, file_utils
import os

bp = Blueprint('manager', __name__)


""" Фильтрация задач по статусу """
def filter_tasks(user_id, request):
	filter = db.convert_task_status(request.form["task-filter"])
	print(f"Filtering tasks --> {filter}")

	return (db.get_filtered_tasks(user_id, filter), filter)


""" Удаление пустых значений """
@bp.app_template_filter('whitespaces')
def remove_whitespaces(s):
	if len(s) == 1:
		return ""
	return s


@bp.route('/')
def index():
	return render_template("home.html")


@bp.route('/main', methods=("GET", "POST"))
@auth.login_required
def main():
	if request.method == "POST":
		tasks, template = filter_tasks(g.user, request)
	else:
		tasks, template = db.get_user_tasks(g.user), None

	if g.is_admin:
		users = db.get_all_users(g.user)
		print('Redirecting to admin page')
		return render_template("admin/index.html", users=users)
	
	print('Redirecting to user page')
	return render_template("user/index.html", tasks=tasks, filter_template=template)


@bp.route('/add-user', methods=("GET", "POST"))
@auth.login_required
@auth.admin_required
def add_user():
	if request.method == "POST":
		print(f'Adding new user: {request.form}...')
		if request.form["is_admin"] == 'Да':
			is_admin = True
		else:
			is_admin = False

		resp = db.add_new_user(request.form["first_name"], request.form["second_name"],
										request.form["surname"], request.form["username"],
										request.form["password"], is_admin)
		print(resp)
		if resp['status'] != "success":
			flash(resp['status'])
		else:
			return redirect(url_for("main"))
	return render_template("admin/add-user.html", main_page_url=request.referrer)


@bp.route('/add-task', methods=("GET", "POST"))
@auth.login_required
@auth.admin_required
def add_task():
	if request.method == "POST":
		print(f'Adding new task: {request.form}...')

		if 'file' in request.files:
			files_arr = file_utils.preprocess_files(request.files.getlist("file"))
			file_utils.upload_files(files_arr)
			filenames = ";".join([f.filename for f in files_arr])
		else:
			filenames = ";"

		resp = db.add_new_task(
				g.user,
				session["observed_user_id"],
				request.form["title"],
				request.form["body"],
				db.IN_PROGRESS_STATUS,
				"",
				filenames
			)
		if resp['status'] != "success":
			flash(resp['status'])
		else:
			return redirect(url_for("manager.observe_user_tasks", id=session["observed_user_id"]))
	return render_template("admin/add-task.html", main_page_url=request.referrer)


@bp.route('/obs-user/<int:id>', methods=("GET", "POST"))
@auth.login_required
@auth.admin_required
def observe_user_tasks(id):
	session["observed_user_id"] = id
	if request.method == "POST":
		tasks, template = filter_tasks(id, request)
	else:
		tasks, template = db.get_user_tasks(id), None

	return render_template('user/index.html', tasks=tasks, filter_template=template)


@bp.route('/task/<int:id>', methods=("GET", "POST"))
@auth.login_required
def task_page(id):
	task = db.get_task_by_id(id)

	if request.method == "POST":
		new_status = db.convert_task_status(request.form['status'])
		old_status = task[3]
		if new_status != old_status:
			resp = db.update_task_status(id, new_status)
			print(f'Updating post`s id = {id} status to {new_status}: {resp["status"]}')

		new_deadline = request.form['deadline']
		old_deadline = task[4]
		if len(new_deadline) > 1 and new_deadline != old_deadline:
			resp = db.update_task_deadline(id, new_deadline)
			print(f'Updating post`s id = {id} deadline to {new_deadline}: {resp["status"]}')

		if 'file' in request.files:
			files_arr = file_utils.preprocess_files(request.files.getlist("file"))
			if len(files_arr) != 0:
				file_utils.upload_files(files_arr)
				filenames = ";".join([f.filename for f in files_arr])
				resp = db.update_task_files(id, filenames)
				print(f"Updating task files: {resp['status']}")
		return redirect(url_for("main"))

	print(f'Redirecting to task {id}')
	files = db.get_task_files(id)
	author = db.get_user_by_id(task["author_id"])
	return render_template("task-page.html", task=task, author=author,
												files=files, main_page_url=request.referrer)


@bp.route('/delete-user/<int:id>/')
@auth.login_required
@auth.admin_required
def delete_user(id):
	print(f'Deleting user with id = {id}')
	print(db.delete_user(id))
	return redirect(url_for("main"))


@bp.route('/delete-task/<int:id>')
@auth.login_required
@auth.admin_required
def delete_task(id):
	print(f'Deleting task with id = {id}')
	print(db.delete_task(id))
	return redirect(f"/obs-user/{session['observed_user_id']}")

@bp.route('/download/<path:filename>', methods=("GET",))
def get_file(filename):
	storage_path = os.path.join(current_app.root_path, current_app.config['UPLOADED_FILES_DEST'])
	print(f"Downloading {filename}")
	return send_from_directory(storage_path, filename)