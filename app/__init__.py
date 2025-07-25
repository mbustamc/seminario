from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://flaskuser:flaskpass@db/flaskdb'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    
    # Importar modelos después de inicializar db
    from . import models
    
    # Crear tablas
    with app.app_context():
        db.create_all()
    
    # Registrar blueprints
    from . import routes
    app.register_blueprint(routes.main)
    
    return app  # ¡Asegúrate de retornar la app!