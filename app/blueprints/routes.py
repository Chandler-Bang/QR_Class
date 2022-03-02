from app import app
from app import db
import click
import pymysql


@app.cli.command()
def addUser():
    j = 123
    for i in range(10):
        teacher = Teacher()
        student = Student()
        teacher_info = UserInfo(
                username=str(j), role="老师"
        )
        student_info = UserInfo(
                username=str(j), role="学生"
        )
        j += 1
        teacher.user = teacher_info
        Student.user = student_info
        teacher_info.generate_password('123456')
        student_info.generate_password('123456')
        db.session.add(teacher_info)
        db.session.add(student_info)
        db.session.add(student)
        db.session.add(teacher)
        db.session.commit()
        click.echo('adding teacher and stduent')
    click.echo('adding teacher and student done!')




