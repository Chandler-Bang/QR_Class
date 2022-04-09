import qrcode
from app.blueprints import auth_bp
from flask import redirect
from flask import request
from flask import url_for
from flask import flash
from flask import render_template
from flask_login import login_user, login_required, logout_user, current_user
from app.forms import TeacherLogin
from app.forms import StudentLogin
from app.forms import questionAnswerForm
from app.forms import startAnswerForm
from app.models import UserInfo
from app.models import AnswerRecord
from app.models import Role
import pymysql


@auth_bp.route('/', methods=['GET', 'POST'])
def questionAnswer():
    form = questionAnswerForm()
    flash('答题开始')
    if form.validate_on_submit():
        from app.models import db
        if form.choice1.data == 'A':
            record = AnswerRecord(
                    choice1=1
                    )
        if form.choice1.data == 'B':
            record = AnswerRecord(
                    choice2=1
                    )
        if form.choice1.data == 'C':
            record = AnswerRecord(
                    choice3=1
                    )
        if form.choice1.data == 'D':
            record = AnswerRecord(
                    choice4=1
                    )
        db.session.add(record)
        db.session.commit()
    return render_template('questionAnswer.html', form=form)


@auth_bp.route('/teacher/login', methods=['GET', 'POST'])
def teacherLogin():
    if current_user.is_authenticated:
        flash('您已登录')
        return redirect(teacher_redirect_url())
    form = TeacherLogin()
    if form.validate_on_submit():
        role_teacher = Role.query.filter_by(name='teacher').first()
        user_teachers = UserInfo.query.filter_by(role_id=role_teacher.id)
        user_teacher = \
            user_teachers.filter_by(username=form.username.data).first()
        
        if user_teacher and user_teacher.validate_password(form.password.data):
            login_user(user_teacher)
            return redirect(
                    url_for('teacher.addSubject', teacher_id=user_teacher.id)
                    )
        else:
            flash('帐号或密码输入错误')
    return render_template("teacher/teacherLogin.html", form=form)


@auth_bp.route('/student/login', methods=['GET', 'POST'])
def studentLogin():
    if current_user.is_authenticated:
        flash('您已登录')
        return redirect(student_redirect_url())
    form = StudentLogin()
    if form.validate_on_submit():
        role_student = Role.query.filter_by(name='student').first()
        user_students = UserInfo.query.filter_by(role_id=role_student.id)
        user_student = \
            user_students.filter_by(username=form.username.data).first()
        if user_student is None or \
                not user_student.validate_password(form.password.data):
            flash('帐号或密码输入错误')
            return redirect(url_for('auth.studentLogin'))
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


def teacher_redirect_url(default='teacher.addSubject'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default, teacher_id=current_user.id)


def student_redirect_url(default='student.studentIndex'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default, student_id=current_user.id)
