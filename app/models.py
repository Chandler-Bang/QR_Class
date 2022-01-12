from app import db


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter = db.Column(db.String(64), index=True, nullable=False)
    questionText = db.Column(db.Text(254), nullable=False)
    difficulity = db.Column(db.Float(2), nullable=False)
    addTime = db.Column(db.Date(), nullable=False)
    addPerson = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(10), index=True, nullable=False)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subjectName = db.Column(db.String(10), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))


class MutipleChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice1 = db.Column(db.String(20), nullable=False)
    choice2 = db.Column(db.String(20), nullable=False)
    choice3 = db.Column(db.String(20), nullable=False)
    choice4 = db.Column(db.String(20), nullable=False)
    answer = db.Column(db.String(1), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))


class FillInTheBlanks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text(100), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))


class BrifeAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text(100), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
