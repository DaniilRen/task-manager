from werkzeug.utils import secure_filename
from flask import flash, redirect, url_for, current_app
import os


def allowed_file(filename):
	""" Функция проверки расширения файла """
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


def upload_file(request):
	file = request.files['file']
	if file.filename == '':
		error = 'Нет выбранного файла'
		flash(error)
		return {"success": False, "error": error}
	
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(current_app.config["UPLOADED_FILES_DEST"], filename))
		return {"success": True}
	
	error = "Расширение не поддерживается"
	return {"success": False, "error": error}