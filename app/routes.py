from app import app
from flask import render_template
from app.forms import AddQuestionForm


@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")


@app.route('/addQuestion')
def addQuestion():
    form = AddQuestionForm()

    return render_template('addQuestion.html', form=form)


@app.route('/generateQR')
def generateQR():
    return "generateQR"


@app.route('/questionSelect')
def questionSelect():
    return "questionSelect"
