from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class UserInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(10))
    teachers = db.relationship('Teacher', back_populates="user")
    students = db.relationship('Student', back_populates="user")

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


# 老师和科目是多对多
teacher_subject = db.Table(
    'teacher_subject', db.Column(
        'teacher_id', db.Integer, db.ForeignKey('teacher.id')
    ), db.Column(
        'subject_id', db.Integer, db.ForeignKey('subject.id')
    )
)


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    user = db.relationship('UserInfo', back_populates='teachers')
    # 老师和班级是一对多
    classes = db.relationship('Classes', back_populates="teachers")
    subjects = db.relationship(
        'Subject', secondary=teacher_subject, back_populates="teachers"
    )


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subjectName = db.Column(db.String(10), nullable=False)
    # 学科和班级一对一
    classes_id = db.Column(db.ForeignKey('classes.id'))
    classes = db.relationship('Classes')
    chapters = db.relationship('Chapter', back_populates="subject")
    teachers = db.relationship(
        'Teacher', secondary=teacher_subject, back_populates="subjects"
    )


# 学生和班级是多对多
students_classes = db.Table(
        "students_classes",
        db.Column(
            "student_id", db.Integer, db.ForeignKey('student.id')
        ),
        db.Column(
            "classes_id", db.Integer, db.ForeignKey('classes.id')
        ),
    )


class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.ForeignKey('teacher.id'))
    teachers = db.relationship('Teacher', back_populates="classes")
    students = db.relationship(
            'Student', secondary=students_classes, back_populates="classes"
    )


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    user = db.relationship('UserInfo', back_populates='students')
    grade = db.relationship('StudentGrade', back_populates='students')
    classes = db.relationship(
            'Classes', secondary=students_classes, back_populates="students"
    )


class StudentGrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    exampaper_id = db.Column(db.Integer, db.ForeignKey('exam_paper.id'))
    # 成绩和学生、试卷是一对多
    students = db.relationship('Student', back_populates="grade")
    exampapers = db.relationship('ExamPaper', back_populates="grade")


# Question和 Chapter的关联表
chapter_question = db.Table(
    'chapter_question', db.Column(
        'chapter_id', db.Integer, db.ForeignKey('chapter.id')
    ), db.Column(
        'question_id', db.Integer, db.ForeignKey('question.id')
    )
)


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapterName = db.Column(db.String(5), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    subject = db.relationship('Subject', back_populates="chapters")
    questions = db.relationship('Question', secondary=chapter_question,
                                back_populates='chapters')


# 试卷和问题是多对多
exampaper_question = db.Table(
    'exampaper_question',
    db.Column(
        'exampaper_id', db.Integer, db.ForeignKey('exam_paper.id')
        ),
    db.Column(
        'question_id', db.Integer, db.ForeignKey('question.id')
        )
    )


class ExamPaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questions = db.relationship(
        'Question', secondary=exampaper_question, back_populates='exampapers'
    )
    grade = db.relationship('StudentGrade', back_populates="exampapers")


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questionText = db.Column(db.Text(254), nullable=False)
    difficulity = db.Column(db.Float(2), nullable=False)
    addTime = db.Column(db.Date(), nullable=False)
    addPerson = db.Column(db.String(10), nullable=False)
    exampapers = db.relationship(
        'ExamPaper', secondary=exampaper_question, back_populates='questions'
    )
    type = db.Column(db.String(10), index=True, nullable=False)
    chapters = db.relationship(
        'Chapter', secondary=chapter_question, back_populates='questions'
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


#db.drop_all()
db.create_all()
