import click
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_qrcode import QRcode
from config import Config
from flask_login import LoginManager
db = SQLAlchemy()
login = LoginManager()
qr = QRcode()


def create_app(config_name=Config):
    app = Flask(__name__)
    qr.init_app(app)
    app.config.from_object(config_name)
    db.init_app(app)
    from app.blueprints import teacher_bp
    from app.blueprints import student_bp
    from app.blueprints import auth_bp
    app.register_blueprint(teacher_bp, url_prefix='/teacher/<int:teacher_id>')
    app.register_blueprint(student_bp, url_prefix='/student/<int:student_id>')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    from app import models
    register_user(app)
    register_login(app)
    with app.app_context():
        pass
        # db.drop_all()
        db.create_all()
    return app


def register_user(app):
    from app.models import Role

    @app.cli.command()
    def init():
        click.echo('Initializing roles')
        Role.init_role()
        click.echo('Done')

    @app.cli.command()
    def addUser():
        from app.models import Student
        from app.models import Teacher
        from app.models import UserInfo
        from app.models import db
        role_teacher = Role.query.filter_by(name='teacher').first()
        role_student = Role.query.filter_by(name='student').first()
        j = 123
        k = 200
        for i in range(10):
            teacher = Teacher()
            student = Student()
            teacher_info = UserInfo(
                    username=str(j), role_id=role_teacher.id
            )
            student_info = UserInfo(
                    username=str(k), role_id=role_student.id
            )
            j += 1
            k += 1
            teacher.user = teacher_info
            student.user = student_info
            teacher_info.generate_password('123456')
            student_info.generate_password('123456')
            db.session.add(teacher_info)
            db.session.add(student_info)
            db.session.add(student)
            db.session.add(teacher)
            db.session.commit()
            click.echo('adding teacher and stduent')
        click.echo('adding teacher and student done!')


def register_login(app):
    login.init_app(app)
