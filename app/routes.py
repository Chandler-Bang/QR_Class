from app import app
from flask import render_template, redirect, url_for
from app.forms import AddQuestionForm, AddSubjectForm, AddChapterForm


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/addSubject', methods=['GET', 'POST'])
def addSubject():
    form = AddSubjectForm()
    if form.validate_on_submit():
        print('123333')
        return redirect(url_for('addChapter'))
    return render_template('addSubject.html', form=form)


@app.route('/addChapter', methods=['GET', 'POST'])
def addChapter():
    form = AddChapterForm()
    if form.validate_on_submit():
        return redirect(url_for('addQuestion'))
    return render_template('addChapter.html', form=form)


@app.route('/addQuestion', methods=['GET', 'POST'])
def addQuestion():
    form = AddQuestionForm()

    return render_template('addQuestion.html', form=form)


@app.route('/generateQR')
def generateQR():
    return "generateQR"


@app.route('/questionSelect')
def questionSelect():
    return "questionSelect"
