from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField, SelectField, FloatField
from wtforms import DateTimeField, IntegerField, StringField
from wtforms.validators import DataRequired
from datetime import datetime


class AddQuestionForm(FlaskForm):
    type = SelectField(label='题目类型', choices=['选择题', '填空题',  '简答题'])
    chapter = StringField(label='章节')  # 有待完善
    questionText = StringField(label='题目正文', validators=[DataRequired()])
    choice1 = StringField(label='A')
    choice2 = StringField(label='B')
    choice3 = StringField(label='C')
    choice4 = StringField(label='D')
    answer = StringField(label='答案')
    difficulity = FloatField(label='难度选择')
    addTime = DateTimeField(label='添加时间', default=datetime.utcnow())
    addPerson = StringField(label='添加人')
    submit = SubmitField(label='提交')
