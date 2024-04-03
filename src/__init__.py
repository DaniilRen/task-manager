from flask import Flask
from . import manager, auth, db
import os


def create_app():
	app = Flask(__name__)
	
	app.config.from_mapping(
		SECRET_KEY=os.urandom(24),
		DATABASE=os.path.join(os.getcwd(), "src/data.sqlite")
		)

	app.register_blueprint(auth.bp)
	app.register_blueprint(manager.bp)

	app.add_url_rule("/", endpoint="index")

	db.init_app(app)

	return app
