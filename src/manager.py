from flask import render_template, g, Blueprint, request, url_for, redirect
from . import auth, db

bp = Blueprint('manager', __name__)


@bp.route('/')
@auth.login_required
def index():
	if g.is_admin:
		tasks = db.get_all_tasks()
		for task in tasks:
			print(task['author'], task['title'], task['body'])
		return render_template("admin/admin_panel.html", tasks=tasks)
	return render_template("user/index.html")


bp.route('/create', methods=("GET", "POST"))
@auth.login_required
def create():
	if request.method == "POST":
		db.add_new_user(request.form["first_name"], request.form["second_name"],
										request.form["surname"], request.form["login"],
										request.form["password"], request.form["is_admin"])
		return redirect(url_for("/"))