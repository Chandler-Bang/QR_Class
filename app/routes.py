from asyncio import QueueEmpty
from cgi import print_directory
from app import app
from app import db
from flask import render_template, redirect, url_for, request
from app.forms import AddQuestionForm, AddSubjectForm, AddChapterForm
from app.models import Subject, Chapter, Question, MutipleChoice, \
                       FillInTheBlanks, BrifeAnswers


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


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


@app.route('/addChapter/', defaults={'subject_id': '#'}, methods=['GET', 'POST'])
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
        return redirect(url_for('addQuestion', chapter_id=chapter.id))
    return render_template('addChapter.html', form=form, chapter=chapter)


@app.route('/addQuestion', defaults={'chapter_id': '#'}, methods=['GET', 'POST'])
@app.route('/addQuestion/<int:chapter_id>', methods=['GET', 'POST'])
def addQuestion(chapter_id):
    chapter = Chapter.query.get(chapter_id)
    form = AddQuestionForm()
    que = Question.query.all()  # 测试 所用变量
    if form.validate_on_submit():
        question = Question(questionText=form.questionText.data,
                            difficulity=form.difficulity.data,
                            addTime=form.addTime.data,
                            addPerson=form.addPerson.data,
                            type=request.form.get('select'))
        print(request.form.get('select'))
        question.chapters.append(chapter)
        db.session.add(question)
        db.session.commit()
        qst = chapter.questions[0]  # 此处有待完善
        print(qst.id)
        type = request.form.get('select')
        print(type)
        if type == "选择题":
            mutipleChoice = MutipleChoice(choice1=form.choice1.data,
                                          choice2=form.choice2.data,
                                          choice3=form.choice3.data,
                                          choice4=form.choice4.data,
                                          answer=form.answer.data)
            mutipleChoice.question_id = qst.id
            db.session.add(mutipleChoice)
            db.session.commit()
        elif type == "填空题":
            fillInTheBlank = FillInTheBlanks(answer=form.answer.data)
            fillInTheBlank.question_id = qst.id
            db.session.add(fillInTheBlank)
            db.session.commit()
        else:
            brifeAnswer = BrifeAnswers(answer=form.answer.data)
            brifeAnswer.question_id = qst.id
            db.session.add(brifeAnswer)
            db.session.commit()
        return redirect(url_for('showQuestion'))
    return render_template('addQuestion.html', form=form, que=que)


@app.route('/showQuestion')
def showQuestion():
    return render_template('showQuestion.html')


@app.route('/generateQR')
def generateQR():
    return "generateQR"


@app.route('/questionSelect')
def questionSelect():
    return "questionSelect"
