from flask import Flask
from app.core.config import Config
from app.core.extensions import db, migrate, jwt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    
    # Register API blueprints
    from app.api.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    @app.route("/health")
    def health():
        return {"status": "ok", "message": "IoT Platform Running"}
        
    return app
