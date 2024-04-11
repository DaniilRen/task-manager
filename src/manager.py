from flask import render_template, g, Blueprint, request, url_for, redirect, flash, session
from . import auth, db, files

bp = Blueprint('manager', __name__)


def filter_tasks(user_id, request):
	filter = request.form["task-filter"]
	if filter == "0": 
		filter = db.IN_PROGRESS_STATUS
	elif filter == "1":
		filter = db.DONE_STATUS
	else: filter = db.ALL_TASKS
	print(f"Filtering tasks --> {filter}")

	return (db.get_filtered_tasks(user_id, filter), filter)


@bp.route('/')
def index():
	return render_template("home.html")


@bp.route('/main', methods=("GET", "POST"))
@auth.login_required
def main():
	if request.method == "POST":
		tasks, template =filter_tasks(g.user, request)
	else:
			tasks, template = db.get_user_tasks(g.user), None

	if g.is_admin:
		users = db.get_all_users()
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
		if not resp['success']:
			flash(resp['error'])
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
			resp = files.upload_file(request)
			print(f"File upload: {resp}")

		resp = db.add_new_task(g.user,
													session["observed_user_id"],
													request.form["title"],
													request.form["body"],
													db.IN_PROGRESS_STATUS)
		print(resp)
		if not resp['success']:
			flash(resp['error'])
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


@bp.route('/task-page/<int:id>', methods=("GET", "POST"))
@auth.login_required
def task_page(id):
	if request.method == "POST":
		new_status = request.form['status']
		print(f'Updating post`s id = {id} status to {new_status}')
		resp = db.update_task(id, new_status)
		print(resp)
		if not resp['success']:
			flash("Ошибка при обновлении статуса")
		else:
			redirect(url_for("main"))

	print(f'Redirecting to task {id}')
	task = db.get_task_by_id(id)
	author = db.get_user_by_id(task["author_id"])
	return render_template("task-page.html", task=task, author=author, main_page_url=request.referrer)


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