from flask import render_template, g, Blueprint
from peewee import *
from . import auth, db

bp = Blueprint('manager', __name__)


@bp.route('/')
@auth.login_required
def index():
	if g.is_admin:
		tasks = db.get_all_tasks()
		return render_template("admin/admin_panel.html", tasks=tasks)
	return render_template("user/index.html")
