from flask import url_for, render_template, redirect, flash, abort
from flask import Blueprint, g, session, request
import bcrypt
import functools
import logging
from db import *

bp = Blueprint('auth', __name__, url_prefix='/auth')


def login_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
			if g.user is None and g.type is None:
					return redirect(url_for("auth.login"))

			return view(**kwargs)

	return wrapped_view


def super_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
			if g.type not in ['customer', 'admin']:
				abort(403)

			return view(**kwargs)

	return wrapped_view



def admin_required(view):
	@functools.wraps(view)
	def wrapped_view(**kwargs):
			if g.type != 'admin':
				abort(403)

			return view(**kwargs)

	return wrapped_view


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    g.type = session.get("type")
    
    if user_id is None:
    		g.user = None
    else:
    		g.user = (get_user_by_id(user_id)['id'])


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = get_user_by_name(username)
        
        if user is None:
            error = 'Неверное имя пользователя'
        elif not bcrypt.hashpw(password.encode(), user['password']) == user['password']:
            error = 'Неверный пароль'
        
        if error is None:
        	session['user_id'] = user['id']
        	session['type'] = user['type']
        	return redirect(url_for("main"))
            
        flash(error)
    
    return render_template('login.html')


@bp.route("/logout")
def logout():
	session.clear()
	return redirect(url_for("index"))
