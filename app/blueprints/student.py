from app.blueprints import student_bp
from flask import redirect, request
from flask import url_for, flash
from flask import render_template
from flask_login import current_user
from app.forms import StudentLogin
from app.models import Classes
from app.models import UserInfo, Student
import  pymysql


@student_bp.route(
        '/index',
        methods=['GET', 'POST']
    )
def studentIndex(student_id=0):
    student = Student.query.filter_by(student_id=student_id).first()
    classes = Classes.query.all()
    length = len(classes)
    return render_template(
            'student/showClasses.html',
            classes=classes, length=length,
            student_id=student_id, zip=zip,
            student=student, len=len
            )


@student_bp.route('/addToClass/<int:class_id>', methods=['GET', 'POST'])
def addToClass(student_id=0, class_id=0):
    from app.models import db
    student = Student.query.filter_by(student_id=student_id).first()
    classes = Classes.query.get(class_id)
    studentNum = len(classes.students)
    if studentNum >= classes.studentCount:
        flash('当前班级人数已满')
        return redirect(redirect_url())
    student.classes.append(classes)
    db.session.add(student)
    db.session.commit()
    return redirect(redirect_url())


@student_bp.route('/deleteFormClass/<int:class_id>', methods=['GET', 'POST'])
def deleteFromClass(student_id=0, class_id=0):
    from app.models import db
    student = Student.query.filter_by(student_id=student_id).first()
    classes = Classes.query.get(class_id)
    student.classes.remove(classes)
    db.session.add(student)
    db.session.commit()
    return redirect(redirect_url())


def redirect_url(default='student.studentIndex'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default, student_id=current_user.id)
