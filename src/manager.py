from flask import render_template, g, Blueprint, request, url_for, redirect
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
		return render_template("admin/index.html", users=users)
	tasks = db.get_all_tasks()
	return render_template("user/index.html", tasks=tasks)


@bp.route('/add-user', methods=("GET", "POST"))
@auth.login_required
def add_user():
	if request.method == "POST":
		print('Got form request -->', request.form)
		if request.form["is_admin"] == 'Да':
			is_admin = True
		else:
			is_admin = False

		print(db.add_new_user(request.form["first_name"], request.form["second_name"],
										request.form["surname"], request.form["username"],
										request.form["password"], is_admin))
		return redirect(url_for("main"))
	return render_template("admin/add_user.html")


@bp.route('/task-page')
@auth.login_required
def task_page():
	return render_template("task-page.html")


@bp.route('/<int:id>/delete-user')
@auth.login_required
def delete_user(id):
	print(db.delete_user(id))
	return redirect(url_for("main"))


@bp.route('/<int:id>/delete-task')
@auth.login_required
def delete_task(id):
	print(db.delete_task(id))
	return redirect(url_for("main"))