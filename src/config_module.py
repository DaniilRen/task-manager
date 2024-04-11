import json
import os

with open("src/config.json") as file:
	CONFIG_FILE = json.load(file)


class Config(object):
	SECRET_KEY = os.urandom(24)


class DevelopmentConfig(Config):
	global CONFIG_FILE
	DATABASE = os.path.join(os.getcwd(), CONFIG_FILE["DATABASE"])
	UPLOADED_FILES_DEST = CONFIG_FILE["UPLOADED_FILES_DEST"]
	ALLOWED_EXTENSIONS = CONFIG_FILE["ALLOWED_EXTENSIONS"]