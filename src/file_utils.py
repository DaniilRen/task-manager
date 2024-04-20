from werkzeug.utils import secure_filename
from flask import current_app
import os
import time
import random
import string


""" Проверка расширения файла """
def allowed_file(filename):
	return '.' in filename and \
			filename.rsplit('.', 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]


""" Замена некорректного названия """
def replace_wrong_filename(file):
	filename = file.filename
	filename.replace(" ", "_")
	file_data = filename.split(".")
	if len(file_data) != 2:
		return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(16)) + "." + file_data[-1]
	return filename


""" Добавление временной метки файла """
def add_timestamp(filename):
	name, ext = filename.split(".")
	timestamped = name + "_" + time.strftime("%Y%m%d-%H%M%S") + "." + ext
	return timestamped


""" Фильтрация файлов и корректировка названий """
def preprocess_files(files_arr):
	filtered = []
	for file in files_arr:
		filename = add_timestamp(replace_wrong_filename(file))
		if allowed_file(filename):
			file.filename = filename
			filtered.append(file)
	return filtered


""" Добавление файла """
def upload_file(file):
	try:
		storage_path = os.path.join(current_app.root_path, current_app.config['UPLOADED_FILES_DEST'])
		file.save(os.path.join(storage_path, file.filename))
	except Exception as e:
		return {"status": e}
	return {"status": "success"}


""" Добавление нескольких файлов """
def upload_files(files_arr):
	for file in files_arr:
		resp = upload_file(file)
		print(f"Uploading {file.filename}: {resp['status']}")