from flask import render_template, g, Blueprint, request, url_for, redirect, flash
from . import auth, db

bp = Blueprint('manager', __name__)


@bp.route('/')
def index():
	return render_template("home.html")


@bp.route('/main')
@auth.login_required
def main():
	if g.is_admin:
		users = db.get_all_users()
		print('Redirecting to admin page')
		return render_template("admin/index.html", users=users)
	tasks = db.get_all_tasks()
	print('Redirecting to user page')
	return render_template("user/index.html", tasks=tasks)


@bp.route('/add-user', methods=("GET", "POST"))
@auth.login_required
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
	return render_template("admin/add-user.html")


@bp.route('/see-user', methods=('POST',))
def see_user_tasks(id):
	render_template('user/index.html')


@bp.route('/<int:id>/task-page', methods=("GET", "POST"))
@auth.login_required
def task_page(id):
	print(request.method)
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
	return render_template("task-page.html", task=db.get_task_by_id(id))


@bp.route('/<int:id>/delete-user')
@auth.login_required
def delete_user(id):
	print(f'Deleting user with id = {id}')
	print(db.delete_user(id))
	return redirect(url_for("main"))


@bp.route('/<int:id>/delete-task')
@auth.login_required
def delete_task(id):
	print(f'Deleting task with id = {id}')
	print(db.delete_task(id))
	return redirect(url_for("main"))