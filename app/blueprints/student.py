from app.blueprints import student_bp
from flask import redirect
from flask import url_for
from flask import render_template
from app.forms import StudentLogin
from app.models import Classes
from app.models import UserInfo
import  pymysql


@student_bp.route(
        '/index',
        methods=['GET', 'POST']
    )
def studentIndex(student_id=0):
    classes = Classes.query.all()
    length = len(classes)
    return render_template(
            'student/showClasses.html', classes=classes, length=length,
            zip=zip
            )
