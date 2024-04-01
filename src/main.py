import app, db

app = app.create_app()
db.init_db()

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=4001, debug=True)