from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import config

# Inicialização das extensões
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_name='default'):
    """Factory function para criar a aplicação Flask"""
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Registrar blueprints
    from app.routes.auth import auth_bp
    from app.routes.users import users_bp
    from app.routes.calls import calls_bp
    from app.routes.evaluations import evaluations_bp
    from app.routes.dashboard import dashboard_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(calls_bp, url_prefix='/api/calls')
    app.register_blueprint(evaluations_bp, url_prefix='/api/evaluations')
    app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
    
    # Rota de health check
    @app.route('/api/health')
    def health_check():
        return {'status': 'ok', 'message': 'API is running'}
    
    return app
