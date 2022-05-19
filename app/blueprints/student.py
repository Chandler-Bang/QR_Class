from app.blueprints import student_bp
from flask import redirect, request
from flask import url_for, flash
from flask import render_template
from flask_login import current_user, login_required
from app.forms import StudentLogin
from app.models import Classes
from app.models import ExamPaper, Subject
from app.models import UserInfo, Student, StudentGrade
import  pymysql


@student_bp.before_request
@login_required
def login_commit():
    if current_user.is_student():
        pass
    else:
        return render_template('error.html')


@student_bp.errorhandler(401)
def unauthorized(error):
    return render_template('error.html'), 401


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
            student=student, len=len, Subject=Subject
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


@student_bp.route('/showClassesInfo/<int:class_id>', methods=['GET', 'POST'])
def showClassesInfo(student_id=0, class_id=0):
    classes = Classes().query.get(class_id)
    exampapers = classes.exampapers
    length = len(exampapers)
    return render_template(
            'student/showExampapers.html',
            student_id=student_id,
            exampapers=exampapers,
            length=length,
            class_id=class_id,
            len=len,
            zip=zip,
            )


@student_bp.route(
        '/checkExampaper/<int:class_id>/<int:exampaper_id>',
        methods=['GET', 'POST']
        )
def checkExampaper(student_id=0, class_id=0, exampaper_id=0):
    from app.models import db
    exampaper = ExamPaper().query.get(exampaper_id)
    questions = exampaper.questions
    questions_mutipleChoice = []
    questions_fillInTheBlank = []
    if questions:
        for question in questions:
            if question.type == '选择题':
                questions_mutipleChoice.append(question)
            else:
                questions_fillInTheBlank.append(question)
    length_mutipleChoice = len(questions_mutipleChoice)
    length_fillInTheBlank = len(questions_fillInTheBlank)
    if request.method == 'POST':
        classes_id = Classes().query.get(class_id).classes_id
        student_grade_record = StudentGrade.query.filter(
                StudentGrade.student_id == student_id,
                StudentGrade.exampaper_id == exampaper_id,
                StudentGrade.classes_id == classes_id
                ).first()
        if student_grade_record:
            flash('您已经做过该试卷了')
        else:
            grade = 0
            for question_mutipleChoice in questions_mutipleChoice:
                question_obj = question_mutipleChoice.mutipleChoice
                id = str(question_obj.id)
                selected_answer = request.form.get(id)
                if selected_answer == question_obj.choice1:
                    selected_answer = 'A'
                elif selected_answer == question_obj.choice2:
                    selected_answer = 'B'
                elif selected_answer == question_obj.choice3:
                    selected_answer = 'C'
                else:
                    selected_answer = 'D'
                if selected_answer == question_obj.answer:
                    grade += 5
                    print('cool')
                else:
                    print('ops')
            for question_fillInTheBlank in questions_fillInTheBlank:
                question_obj = question_fillInTheBlank.fillInTheBlanks
                id = str(question_obj.id)
                selected_answer = request.form.get(id)
                if selected_answer == question_obj.answer:
                    grade += 5
                    print('cool')
                else:
                    print('ops')
            student_grade = StudentGrade(
                    grade=grade
                    )
            student_grade.student_id = student_id
            student_grade.classes_id = classes_id
            student_grade.exampaper_id = exampaper_id
            db.session.add(student_grade)
            db.session.commit()
    return render_template(
            'student/checkExampaper.html',
            student_id=student_id,
            class_id=class_id,
            exampaper_id=exampaper_id,
            questions_mutipleChoice=questions_mutipleChoice,
            questions_fillInTheBlank=questions_fillInTheBlank,
            length_mutipleChoice=length_mutipleChoice,
            length_fillInTheBlank=length_fillInTheBlank,
            zip=zip
            )


@student_bp.route(
        '/listExampaper/<int:class_id>/<int:exampaper_id>',
        methods=['GET', 'POST']
        )
def listExampaper(student_id=0, class_id=0, exampaper_id=0):
    from app.models import db
    if student_id == 0:
        student_id = current_user.id
    exampaper = ExamPaper().query.get(exampaper_id)
    questions = exampaper.questions
    questions_mutipleChoice = []
    questions_fillInTheBlank = []
    if questions:
        for question in questions:
            if question.type == '选择题':
                questions_mutipleChoice.append(question)
            else:
                questions_fillInTheBlank.append(question)
    length_mutipleChoice = len(questions_mutipleChoice)
    length_fillInTheBlank = len(questions_fillInTheBlank)
    if request.method == 'POST':
        classes_id = Classes().query.get(class_id).classes_id
        student_grade_record = StudentGrade.query.filter(
                StudentGrade.student_id == student_id,
                StudentGrade.exampaper_id == exampaper_id,
                StudentGrade.classes_id == classes_id
                ).first()
        if student_grade_record:
            flash('您已经做过该试卷了')
        else:
            grade = 0
            for question_mutipleChoice in questions_mutipleChoice:
                question_obj = question_mutipleChoice.mutipleChoice
                id = str(question_obj.id)
                selected_answer = request.form.get(id)
                if selected_answer == question_obj.choice1:
                    selected_answer = 'A'
                elif selected_answer == question_obj.choice2:
                    selected_answer = 'B'
                elif selected_answer == question_obj.choice3:
                    selected_answer = 'C'
                else:
                    selected_answer = 'D'
                if selected_answer == question_obj.answer:
                    grade += 5
                    print('cool')
                else:
                    print('ops')
            for question_fillInTheBlank in questions_fillInTheBlank:
                question_obj = question_fillInTheBlank.fillInTheBlanks
                id = str(question_obj.id)
                selected_answer = request.form.get(id)
                if selected_answer == question_obj.answer:
                    grade += 5
                    print('cool')
                else:
                    print('ops')
            student_grade = StudentGrade(
                    grade=grade
                    )
            student_grade.student_id = student_id
            student_grade.classes_id = classes_id
            student_grade.exampaper_id = exampaper_id
            db.session.add(student_grade)
            db.session.commit()
    return render_template(
            'student/checkExampaper.html',
            student_id=student_id,
            class_id=class_id,
            exampaper_id=exampaper_id,
            questions_mutipleChoice=questions_mutipleChoice,
            questions_fillInTheBlank=questions_fillInTheBlank,
            length_mutipleChoice=length_mutipleChoice,
            length_fillInTheBlank=length_fillInTheBlank,
            zip=zip
            )


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
