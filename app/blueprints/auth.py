from app.blueprints import auth_bp
from flask import redirect
from flask import url_for
from flask import render_template
from flask_login import login_user, login_required, logout_user, current_user
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
        user_teachers = UserInfo.query.filter_by(role_id=role_teacher.id)
        user_teacher = \
            user_teachers.filter_by(username=form.username.data).first()
        flag = user_teacher.validate_password(form.password.data)
        if flag:
            login_user(user_teacher)
            return redirect(
                    url_for('teacher.addSubject', teacher_id=user_teacher.id)
                    )
    return render_template("teacher/teacherLogin.html", form=form)


@auth_bp.route('/student/login', methods=['GET', 'POST'])
def studentLogin():
    form = StudentLogin()
    if form.validate_on_submit():
        role_student = Role.query.filter_by(name='student').first()
        user_students = UserInfo.query.filter_by(role_id=role_student.id)
        user_student = \
            user_students.filter_by(username=form.username.data).first()
        flag = user_student.validate_password(form.password.data)
        if flag:
            login_user(user_student)
            return redirect(
                    url_for('student.studentIndex', student_id=user_student.id)
                    )
    return render_template("student/studentLogin.html", form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    if current_user.is_teacher():
        logout_user()
        return redirect(url_for('auth.teacherLogin'))
    if current_user.is_student():
        logout_user()
        return redirect(url_for('auth.studentLogin'))
