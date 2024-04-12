from werkzeug.utils import secure_filename
from flask import flash, current_app
import os


def allowed_file(filename):
	""" Функция проверки расширения файла """
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


def upload_file(file):
	if file.filename == '':
		error = 'Нет выбранного файла'
		flash(error)
		return {"success": False, "error": error}
	
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		storage_path = os.path.join(current_app.root_path, current_app.config['UPLOADED_FILES_DEST'])
		file.save(os.path.join(storage_path, filename))
		return {"success": True}
	
	error = "Расширение не поддерживается"
	return {"success": False, "error": error}

