from flask import Flask
import manager, auth, db, config_module


def create_app():
    app = Flask(__name__)
    app.config.from_object(config_module.DevelopmentConfig())
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(manager.bp)
    
    app.add_url_rule("/", endpoint="index")
    app.add_url_rule("/main", endpoint="main")
    
    db.init_app(app)
    
    return app
