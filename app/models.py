from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subjectName = db.Column(db.String(10), nullable=False)
    chapters = db.relationship('Chapter', back_populates="subject")


# Question和 Chapter的关联表
association_table = db.Table(
    'association', db.Column(
        'Chapter_id', db.Integer, db.ForeignKey('chapter.id')
    ), db.Column(
        'Question_id', db.Integer, db.ForeignKey('question.id')
    )
)


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapterName = db.Column(db.String(5), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', back_populates="chapters")
    questions = db.relationship('Question', secondary=association_table,
                                back_populates='chapters')


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questionText = db.Column(db.Text(254), nullable=False)
    difficulity = db.Column(db.Float(2), nullable=False)
    addTime = db.Column(db.Date(), nullable=False)
    addPerson = db.Column(db.String(10), nullable=False)
    type = db.Column(db.String(10), index=True, nullable=False)
    chapters = db.relationship(
        'Chapter', secondary=association_table, back_populates='questions'
    )
    mutipleChoice = db.relationship('MutipleChoice', cascade="delete", uselist=False)
    fillInTheBlanks = db.relationship('FillInTheBlanks', cascade="all", uselist=False)
    brifeAnswers = db.relationship('BrifeAnswers', uselist=False)


class MutipleChoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice1 = db.Column(db.String(20), nullable=False)
    choice2 = db.Column(db.String(20), nullable=False)
    choice3 = db.Column(db.String(20), nullable=False)
    choice4 = db.Column(db.String(20), nullable=False)
    answer = db.Column(db.String(1), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question')


class FillInTheBlanks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text(100), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question', cascade="delete")


class BrifeAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    answer = db.Column(db.Text(100), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    question = db.relationship('Question')


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(5), nullable=False)
    password_hash = db.Column(db.String(128))

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


db.drop_all()
db.create_all()
