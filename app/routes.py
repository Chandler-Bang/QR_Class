from asyncio import QueueEmpty
from cgi import print_directory
from app import app
from app import db
import click
from flask import render_template, redirect, url_for, request, flash
from app.forms import AddQuestionForm, AddSubjectForm, AddChapterForm, \
    TeacherLogin, questionAnswerForm, StudentLogin, AddExamPaper, AddClasses
from app.models import Subject, Chapter, Question, MutipleChoice, \
    FillInTheBlanks, Teacher, Student, UserInfo, ExamPaper, Classes
import pymysql


@app.cli.command()
def addUser():
    j = 123
    for i in range(10):
        teacher = Teacher()
        student = Student()
        teacher_info = UserInfo(
                username=str(j), role="老师"
        )
        student_info = UserInfo(
                username=str(j), role="学生"
        )
        j += 1
        teacher.user = teacher_info
        Student.user = student_info
        teacher_info.generate_password('123456')
        student_info.generate_password('123456')
        db.session.add(teacher_info)
        db.session.add(student_info)
        db.session.add(student)
        db.session.add(teacher)
        db.session.commit()
        click.echo('adding teacher and stduent')
    click.echo('adding teacher and student done!')


@app.route(
        '/index/teacher/<int:teacher_id>',
        methods=['GET', 'POST']
    )
def teacherIndex(teacher_id=0):
    from app.models import db
    form = AddClasses(teacher_id)
    if form.validate_on_submit():
        pass
        subject = Subject.query.filter_by(teacher_id=teacher_id).all()
        subject_id = subject.filter_by(
                subjectName=form.subjectName.data
                ).first().id
        classes = Classes(
                classes_id=form.classes_id.data,
                terms=form.terms.data,
                studentCount=form.studentCount.data,
                subject_id=subject_id,
                teacher_id=teacher_id
        )
        db.session.add(classes)
        db.session.commit()
        return redirect(url_for('showClasses', teacher_id=teacher_id))
    return render_template('teacher/addClasses.html', form=form)


@app.route('/teacher/<int:teacher_id>/showClasses', methods=['GET', 'POST'])
def showClasses(teacher_id=0):
    classes = Classes.query.filter_by(teacher_id=teacher_id).all()
    length = len(classes)
    return render_template(
            'teacher/showClasses.html', classes=classes, length=length,
            zip=zip
            )


@app.route(
        '/index/student/<int:student_id>',
        methods=['GET', 'POST']
    )
def studentIndex(student_id=0):
    classes = Classes.query.all()
    length = len(classes)
    return render_template(
            'student/showClasses.html', classes=classes, length=length,
            zip=zip
            )


@app.route('/', methods=['GET', 'POST'])
@app.route('/teacher', methods=['GET', 'POST'])
def teacherLogin():
    form = TeacherLogin()
    if form.validate_on_submit():
        teachers = UserInfo.query.filter_by(role="老师")
        teacher = teachers.filter_by(username=form.username.data)[0]
        flag = teacher.validate_password(form.password.data)
        if flag:
            return redirect(url_for('teacherIndex', teacher_id=teacher.id))
    return render_template("teacher/teacherLogin.html", form=form)


@app.route('/student', methods=['GET', 'POST'])
def studentLogin():
    form = StudentLogin()
    if form.validate_on_submit():
        students = UserInfo.query.filter_by(role="学生")
        student = students.filter_by(username=form.username.data)[0]
        flag = student.validate_password(form.password.data)
        if flag:
            return redirect(url_for('studentIndex', student_id=student.id))
    return render_template("student/studentLogin.html", form=form)


@app.route('/questionAnswer', methods=['GET', 'POST'])
def questionAnswer():
    form = questionAnswerForm()
    if form.validate_on_submit():
        return redirect(url_for('showAnswer'))
    return render_template('questionAnswer.html', form=form)


@app.route('/showAnswer')
def showAnswer():
    return render_template('showAnswer.html')


@app.route('/addSubject', methods=['GET', 'POST'])
def addSubject():
    form = AddSubjectForm()
    subject = Subject.query.all()
    if form.validate_on_submit():
        data = form.subject.data
        subject = Subject(subjectName=data)
        db.session.add(subject)
        db.session.commit()
        id = Subject.query.filter_by(subjectName=data)[0].id
        return redirect(url_for('addChapter', subject_id=id))
    return render_template('teacher/addSubject.html', form=form, subject=subject)


@app.route('/addChapter/<int:subject_id>', methods=['GET', 'POST'])
def addChapter(subject_id=0):
    form = AddChapterForm()
    chapter = Chapter.query.filter_by(subject_id=subject_id)
    if form.validate_on_submit():
        data = form.chapter.data
        chapter = Chapter(chapterName=data)
        subject = Subject.query.get(subject_id)
        chapter.subject = subject
        db.session.add(chapter)
        db.session.commit()
        print(chapter.id)
        return redirect(url_for('showQuestion', chapter_id=chapter.id))
    return render_template('teacher/addChapter.html', form=form, chapter=chapter)


@app.route('/showQuestion/<int:chapter_id>', methods=['GET', 'POST'])
def showQuestion(chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    questions = chapter.questions
    subject_id = chapter.subject_id
    length = len(questions)
    return render_template(
        'teacher/showQuestion.html', questions=questions, chapter_id=chapter_id,
        subject_id=subject_id, length=length, zip=zip
    )


@app.route('/addExamPaper/<int:chapter_id>', methods=['GET', 'POST'])
def addExamPaper(chapter_id):
    from app.models import db
    form = AddExamPaper()
    exampapers = ExamPaper.query.filter_by(chapter_id=chapter_id).all()
    length = len(exampapers)
    if form.validate_on_submit():
        exampaper = ExamPaper(
            name=form.examPaperName.data,
            chapter_id=chapter_id,
            tag=form.examTag.data
        )  
        db.session.add(exampaper)
        db.session.commit()
        return redirect(url_for('addQuestionToExamPaper', chapter_id=chapter_id, exampaper_id=exampaper.id))
    return render_template(
            '/teacher/addExamPaper.html', form=form, exampapers=exampapers,
            chapter_id=chapter_id, length=length, zip=zip
        )


@app.route('/addQuestionToExamPaper/<int:chapter_id>/<int:exampaper_id>', methods=['GET', 'POST'])
def addQuestionToExamPaper(chapter_id=0, exampaper_id=0):
    exampaper = ExamPaper.query.filter_by(id=exampaper_id).first()
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    questions = chapter.questions
    length = len(questions)
    return render_template(
        'teacher/addQuestionToExamPaper.html', questions=questions, chapter_id=chapter_id, length=length, zip=zip, exampaper_id=exampaper_id, exampaper=exampaper
    )


@app.route('/questionAddToExamPaper/<int:exampaper_id>/<int:question_id>', methods=['GET', 'POST'])
def questionAddToExamPaper(exampaper_id=0, question_id=0):
    from app.models import db
    exampaper = ExamPaper.query.get(exampaper_id) 
    question = Question.query.get(question_id)
    print(exampaper)
    exampaper.questions.append(question)
    print(exampaper.questions)
    db.session.add(exampaper)
    db.session.commit()
    return redirect(redirect_url())


@app.route('/questionDeleteFromExamPaper/<int:exampaper_id>/<int:question_id>', methods=['GET', 'POST'])
def questionDeleteFromExamPaper(exampaper_id=0, question_id=0):
    from app.models import db
    exampaper = ExamPaper.query.get(exampaper_id) 
    question = Question.query.get(question_id)
    exampaper.questions.remove(question)
    db.session.commit()
    return redirect(redirect_url())


@app.route('/addQuestion/<int:chapter_id>', methods=['GET', 'POST'])
def addQuestion(chapter_id=0):
    from app.models import db
    chapter = Chapter.query.get(chapter_id)
    form = AddQuestionForm()
    que = Question.query.all()  # 测试 所用变量
    if form.validate_on_submit():
        question = Question(
            questionText=form.questionText.data,
            difficulity=form.difficulity.data,
            type=request.form.get('select')
        )
        question.chapters.append(chapter)
        type = request.form.get('select')
        print(type)
        if type == "选择题":
            mutipleChoice = MutipleChoice(
                choice1=form.choice1.data,
                choice2=form.choice2.data,
                choice3=form.choice3.data,
                choice4=form.choice4.data,
                answer=form.answer.data
            )
            question.mutipleChoice = mutipleChoice
        elif type == "填空题":
            fillInTheBlank = FillInTheBlanks(answer=form.answer.data)
            question.fillInTheBlanks = fillInTheBlank
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('showQuestion', chapter_id=chapter_id))
    return render_template(
        'teacher/addQuestion.html', form=form, que=que, chapter_id=chapter_id
    )


@app.route('/questionDelete/<int:question_id>', methods=['GET', 'POST'])
def questionDelete(question_id):
    from app.models import db
    question = Question.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(redirect_url())


@app.route('/examPaperDelete/<int:exampaper_id>', methods=['GET', 'POST'])
def examPaperDelete(exampaper_id):
    from app.models import db
    exampaper = ExamPaper.query.get(exampaper_id)
    for question in exampaper.questions:
        exampaper.questions.remove(question)
    db.session.delete(exampaper)
    db.session.commit()
    return redirect(redirect_url())


@app.route('/generateQR')
def generateQR():
    return "generateQR"


@app.route('/questionSelect')
def questionSelect():
    return "questionSelect"


def redirect_url(default='index'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default)
