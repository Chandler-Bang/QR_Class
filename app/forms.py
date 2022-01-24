from flask.helpers import flash
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, FloatField
from wtforms import DateTimeField, IntegerField, StringField
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
    addTime = DateTimeField(label='添加时间', default=date.today())
    addPerson = StringField(label='添加人')
    submit = SubmitField(label='提交')
