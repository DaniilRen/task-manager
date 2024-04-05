from flask import render_template, g, Blueprint, request, url_for, redirect
from . import auth, db

bp = Blueprint('manager', __name__)


@bp.route('/')
@auth.login_required
def index():
	if g.is_admin:
		users = db.get_all_users()
		return render_template("admin/admin_panel.html", users=users)
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
		return redirect(url_for("index"))
	return render_template("admin/add_user.html")