from ast import Sub
from cProfile import label
from tokenize import String
from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, FloatField, RadioField
from wtforms import DateTimeField, IntegerField, StringField
from app.models import Subject
from wtforms.validators import DataRequired, Length
from datetime import date


class AddSubjectForm(FlaskForm):
    subject = StringField(label="学科名称",
                          validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField(label="提交")


class AddChapterForm(FlaskForm):
    chapter = StringField(label="章节",
                          validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField(label="提交")


class AddQuestionForm(FlaskForm):
    questionText = StringField(label='题目正文', validators=[DataRequired()])
    choice1 = StringField(label='A')
    choice2 = StringField(label='B')
    choice3 = StringField(label='C')
    choice4 = StringField(label='D')
    answer = StringField(label='答案')
    difficulity = FloatField(label='难度选择')
    submit = SubmitField(label='提交')


class TeacherLogin(FlaskForm):
    username = StringField(label="教师用户名", validators=[DataRequired()])
    password = StringField(label="密码")
    submit = SubmitField(label='登录')


class StudentLogin(FlaskForm):
    username = StringField(label="学生用户名", validators=[DataRequired()])
    password = StringField(label="密码")
    submit = SubmitField(label='登录')


class questionAnswerForm(FlaskForm):
    choice1 = RadioField(
        label='选项如下', choices=[
            ('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')
        ]
    )
    submit = SubmitField(label="提交答案")


class AddExamPaper(FlaskForm):
    examPaperName = StringField(label="试卷名称")
    examTag = TextAreaField(label="试卷描述")
    submit = SubmitField(label="提交")


class AddClasses(FlaskForm):
    year = str(date.today().year)
    classes_id = StringField(label="班级编号")
    subjectName = SelectField(label="学科选择")
    terms = SelectField(
            label="学期选择",
            choices=[(year + '-1', year + '-1'), (year + '-2', year + '-2')]
            )
    studentCount = IntegerField(label='学生人数')
    submit = SubmitField(label="提交")

    def __init__(self, teacher_id):
        super(AddClasses, self).__init__()
        subject = Subject.query.filter_by(teacher_id=teacher_id).all()
        self.subjectName.choices = []
        for subjectValue, subjectDescribe in zip(subject, subject):
            self.subjectName.choices.append((subjectValue.subjectName, subjectDescribe.subjectName))
