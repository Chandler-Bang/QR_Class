from app.blueprints import auth_bp
from flask import redirect
from flask import url_for
from flask import render_template
from flask_login import login_user
from app.forms import TeacherLogin
from app.forms import StudentLogin
from app.models import UserInfo
from app.models import Role
import pymysql


@auth_bp.route('/', methods=['GET', 'POST'])
def teacherLogin():
    form = TeacherLogin()
    if form.validate_on_submit():
        role_teacher = Role.query.filter_by(name='teacher').first()
        teachers = UserInfo.query.filter_by(role_id=role_teacher.id)
        teacher = teachers.filter_by(username=form.username.data)[0]
        flag = teacher.validate_password(form.password.data)
        if flag:
            login_user(teacher)
            return redirect(
                    url_for('teacher.addSubject', teacher_id=teacher.id)
                    )
    return render_template("teacher/teacherLogin.html", form=form)


@auth_bp.route('/student/login', methods=['GET', 'POST'])
def studentLogin():
    form = StudentLogin()
    if form.validate_on_submit():
        students = UserInfo.query.filter_by(role="学生")
        student = students.filter_by(username=form.username.data)[0]
        flag = student.validate_password(form.password.data)
        if flag:
            return redirect(
                    url_for('student.studentIndex', student_id=student.id)
                    )
    return render_template("student/studentLogin.html", form=form)
