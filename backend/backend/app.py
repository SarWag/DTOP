# Main file for running the Flask server
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from backend.models import db

# Import Blueprints
from backend.controller.file_handle_controller import file_handle_controller
from backend.controller.fuzzy_controller import fuzzy_controller
# from backend.services.json_visualizer import json_visualizer
from backend.controller.db_controller import db_controller

# Register application
app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://assistant:admin@172.17.0.2:5432/flask"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://assistant:0000@172.17.0.4:5432/backend"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database integration
db.init_app(app)

migrate = Migrate(app, db)
# with app.app_context():
#     db.create_all()


# Register controllers
# app.register_blueprint(graphdb_controller)
# app.register_blueprint(json_visualizer)
app.register_blueprint(db_controller)
app.register_blueprint(file_handle_controller)
app.register_blueprint(fuzzy_controller)

if __name__ == "__main__":
    app.run()
