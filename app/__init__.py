from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
import os


db = SQLAlchemy()


def create_app(config_name=Config):
    app = Flask(__name__)
    app.config.from_object(config_name)
    db.init_app(app)
    from app.blueprints import teacher_bp
    from app.blueprints import student_bp
    from app.blueprints import auth_bp
    app.register_blueprint(teacher_bp, url_prefix='/teacher/<int:teacher_id>')
    app.register_blueprint(student_bp, url_prefix='/student/<int:student_id>')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app import models
    return app
