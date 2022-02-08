from asyncio import QueueEmpty
from cgi import print_directory
from app import app
from app import db
import click
from flask import render_template, redirect, url_for, request, flash
from app.forms import AddQuestionForm, AddSubjectForm, AddChapterForm, \
    TeacherLogin, questionAnswerForm
from app.models import Subject, Chapter, Question, MutipleChoice, \
    FillInTheBlanks, BrifeAnswers, Teacher
import pymysql


@app.cli.command()
def addTeacher():
    j = 123
    for i in range(10):
        teacher = Teacher(username=str(j))
        j += 1
        teacher.generate_password('123456')
        db.session.add(teacher)
        db.session.commit()
        click.echo('adding teacher')
    click.echo('adding teacher done!')


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    form = TeacherLogin()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        teacher = Teacher.query.filter_by(username=form.username.data)[0]
        flag = teacher.validate_password(form.password.data)
        if flag:
            return redirect(url_for('addSubject'))
    return render_template("index.html", form=form)


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
        id = Subject.query.filter(Subject.subjectName == data)[0].id
        return redirect(url_for('addChapter', subject_id=id))
    return render_template('addSubject.html', form=form, subject=subject)


@app.route(
    '/addChapter/', defaults={'subject_id': '#'}, methods=['GET', 'POST']
    )
@app.route('/addChapter/<int:subject_id>', methods=['GET', 'POST'])
def addChapter(subject_id):
    form = AddChapterForm()
    chapter = Chapter.query.filter_by(subject_id=subject_id)
    if form.validate_on_submit():
        data = form.chapter.data
        chapter = Chapter(chapterName=data)
        subject = Subject.query.get(subject_id)
        chapter.subject = subject
        db.session.add(chapter)
        db.session.commit()
        return redirect(url_for('showQuestion', chapter_id=chapter.id))
    return render_template('addChapter.html', form=form, chapter=chapter)


@app.route('/showQuestion/<int:chapter_id>', methods=['GET', 'POST'])
def showQuestion(chapter_id):
    chapter = Chapter.query.filter_by(id=chapter_id)[0]
    questions = chapter.questions
    subject_id = chapter.subject_id
    return render_template(
        'showQuestion.html', questions=questions, chapter_id=chapter_id,
        subject_id=subject_id
    )


@app.route(
    '/addQuestion', defaults={'chapter_id': '#'}, methods=['GET', 'POST']
    )
@app.route('/addQuestion/<int:chapter_id>', methods=['GET', 'POST'])
def addQuestion(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    form = AddQuestionForm()
    que = Question.query.all()  # 测试 所用变量
    if form.validate_on_submit():
        question = Question(
            questionText=form.questionText.data,
            difficulity=form.difficulity.data,
            addTime=form.addTime.data,
            addPerson=form.addPerson.data,
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
        'addQuestion.html', form=form, que=que, chapter_id=chapter_id
    )


@app.route('/questionDelete/<int:question_id>', methods=['GET', 'POST'])
def questionDelete(question_id):
    question = Question.query.get(question_id)
    db.session.delete(question)
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
