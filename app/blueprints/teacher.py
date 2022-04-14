from app.blueprints import teacher_bp
from flask import url_for, jsonify
from flask import redirect
from flask import g
from flask import render_template
from flask import request
from flask_login import login_user, login_required, current_user
from app.forms import AddClasses
from app.forms import AddSubjectForm
from app.forms import AddChapterForm
from app.forms import AddExamPaper
from app.forms import AddQuestionForm
from app.forms import questionAnswerForm
from app.models import Subject
from app.models import Classes
from app.models import UserInfo
from app.models import Chapter
from app.models import ExamPaper
from app.models import Question
from app.models import MutipleChoice
from app.models import FillInTheBlanks
from app.models import AnswerRecord
import pymysql


@teacher_bp.before_request
@login_required
def login_commit():
    if current_user.is_teacher():
        pass
    else:
        return render_template('error.html')


@teacher_bp.route(
        '/index',
        methods=['GET', 'POST']
    )
def teacherIndex(teacher_id=0):
    from app.models import db
    form = AddClasses(teacher_id)
    if form.validate_on_submit():
        subject = Subject.query.filter_by(teacher_id=teacher_id)
        subject_id = subject.filter_by(
                subjectName=form.subjectName.data
                ).first().id
        classes = Classes(
                classes_id=form.classes_id.data,
                terms=form.terms.data,
                studentCount=form.studentCount.data,
                subject_id=subject_id,
                teacher_id=teacher_id
        )
        db.session.add(classes)
        db.session.commit()
        return redirect(url_for('teacher.showClasses', teacher_id=teacher_id))
    return render_template('teacher/addClasses.html', form=form, redirect_url=redirect_url)


@teacher_bp.route('/showClasses', methods=['GET', 'POST'])
def showClasses(teacher_id=0):
    classes = Classes.query.filter_by(teacher_id=teacher_id).all()
    length = len(classes)
    return render_template(
            'teacher/showClasses.html', classes=classes, length=length,
            zip=zip 
            )


@teacher_bp.route('/addSubject', methods=['GET', 'POST'])
def addSubject(teacher_id=0):
    from app.models import db
    form = AddSubjectForm()
    subject = Subject.query.all()
    if form.validate_on_submit():
        data = form.subject.data
        subject = Subject(
                subjectName=data,
                teacher_id=teacher_id
                )
        db.session.add(subject)
        db.session.commit()
        id = Subject.query.filter_by(subjectName=data)[0].id
        return redirect(
                url_for(
                    'teacher.addChapter', subject_id=id, teacher_id=teacher_id
                    )
                )
    return render_template(
            'teacher/addSubject.html',
            form=form, subject=subject, teacher_id=teacher_id
            )


@teacher_bp.route('/addChapter/<int:subject_id>', methods=['GET', 'POST'])
def addChapter(subject_id=0, teacher_id=0):
    from app.models import db
    form = AddChapterForm()
    chapter = Chapter.query.filter_by(subject_id=subject_id)
    if form.validate_on_submit():
        data = form.chapter.data
        chapter = Chapter(chapterName=data)
        subject = Subject.query.get(subject_id)
        chapter.subject = subject
        db.session.add(chapter)
        db.session.commit()
        print(chapter.id)
        return redirect(
                url_for(
                    'teacher.showQuestion',
                    chapter_id=chapter.id,
                    teacher_id=teacher_id
                    )
                )
    return render_template(
            'teacher/addChapter.html',
            form=form, chapter=chapter, teacher_id=teacher_id
            )


@teacher_bp.route('/showQuestion/<int:chapter_id>', methods=['GET', 'POST'])
def showQuestion(chapter_id=0, teacher_id=0):
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    questions = chapter.questions
    subject_id = chapter.subject_id
    length = len(questions)
    return render_template(
        'teacher/showQuestion.html',
        questions=questions, chapter_id=chapter_id,
        subject_id=subject_id, length=length, zip=zip,
        teacher_id=teacher_id
    )


@teacher_bp.route('/addExamPaper/<int:chapter_id>', methods=['GET', 'POST'])
def addExamPaper(chapter_id=0, teacher_id=0):
    from app.models import db
    form = AddExamPaper()
    exampapers = ExamPaper.query.filter_by(chapter_id=chapter_id).all()
    length = len(exampapers)
    if form.validate_on_submit():
        exampaper = ExamPaper(
            name=form.examPaperName.data,
            chapter_id=chapter_id,
            tag=form.examTag.data
        )
        db.session.add(exampaper)
        db.session.commit()
        return redirect(
                url_for(
                    'teacher.addQuestionToExamPaper',
                    chapter_id=chapter_id,
                    exampaper_id=exampaper.id,
                    teacher_id=teacher_id
                    )
                )
    return render_template(
            '/teacher/addExamPaper.html', form=form, exampapers=exampapers,
            chapter_id=chapter_id,
            length=length, zip=zip, teacher_id=teacher_id
        )


@teacher_bp.route(
        '/addQuestionToExamPaper/<int:chapter_id>/<int:exampaper_id>',
        methods=['GET', 'POST']
        )
def addQuestionToExamPaper(
        chapter_id=0, exampaper_id=0, teacher_id=0
        ):
    exampaper = ExamPaper.query.filter_by(id=exampaper_id).first()
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    questions = chapter.questions
    length = len(questions)
    return render_template(
        'teacher/addQuestionToExamPaper.html',
        questions=questions,
        chapter_id=chapter_id,
        length=length, zip=zip, exampaper_id=exampaper_id,
        exampaper=exampaper,
        teacher_id=teacher_id
    )


@teacher_bp.route(
        '/questionAddToExamPaper/<int:exampaper_id>/<int:question_id>',
        methods=['GET', 'POST']
        )
def questionAddToExamPaper(exampaper_id=0, question_id=0, teacher_id=0):
    from app.models import db
    exampaper = ExamPaper.query.get(exampaper_id)
    question = Question.query.get(question_id)
    exampaper.questions.append(question)
    db.session.add(exampaper)
    db.session.commit()
    return redirect(redirect_url())

@teacher_bp.route(
        '/questionDeleteFromExamPaper/<int:exampaper_id>/<int:question_id>',
        methods=['GET', 'POST']
        )
def questionDeleteFromExamPaper(exampaper_id=0, question_id=0, teacher_id=0):
    from app.models import db
    exampaper = ExamPaper.query.get(exampaper_id)
    question = Question.query.get(question_id)
    exampaper.questions.remove(question)
    db.session.commit()
    return redirect(redirect_url())


@teacher_bp.route('/addQuestion/<int:chapter_id>', methods=['GET', 'POST'])
def addQuestion(chapter_id=0, teacher_id=0):
    from app.models import db
    chapter = Chapter.query.get(chapter_id)
    form = AddQuestionForm()
    que = Question.query.all()  # 测试 所用变量
    print(que)
    if form.validate_on_submit():
        print('hhhh')
        question = Question(
            questionText=form.questionText.data,
            difficulity=form.difficulity.data,
            type=request.form.get('select')
        )
        question.chapters.append(chapter)
        type = request.form.get('select')
        print(type)
        if type == "选择题":
            mutipleChoice = MutipleChoice(
                choice1=form.choice1.data,
                choice2=form.choice2.data,
                choice3=form.choice3.data,
                choice4=form.choice4.data,
                answer=form.answer.data
            )
            question.mutipleChoice = mutipleChoice
        elif type == "填空题":
            fillInTheBlank = FillInTheBlanks(answer=form.answer.data)
            question.fillInTheBlanks = fillInTheBlank
            print(1111)
        db.session.add(question)
        db.session.commit()
        return redirect(
                url_for(
                    'teacher.showQuestion',
                    chapter_id=chapter_id, teacher_id=teacher_id
                    )
                )
    return render_template(
        'teacher/addQuestion.html',
        form=form, que=que, chapter_id=chapter_id, teacher_id=teacher_id
    )


@teacher_bp.route('/questionDelete/<int:question_id>', methods=['GET', 'POST'])
def questionDelete(question_id=0, teacher_id=0):
    from app.models import db
    question = Question.query.get(question_id)
    db.session.delete(question)
    db.session.commit()
    return redirect(redirect_url())


@teacher_bp.route(
        '/examPaperDelete/<int:exampaper_id>', methods=['GET', 'POST']
        )
def examPaperDelete(exampaper_id=0, teacher_id=0):
    from app.models import db
    exampaper = ExamPaper.query.get(exampaper_id)
    for question in exampaper.questions:
        exampaper.questions.remove(question)
    db.session.delete(exampaper)
    db.session.commit()
    return redirect(redirect_url())


@teacher_bp.route('/controlAnswer', methods=['GET', 'POST'])
def controlAnswer(teacher_id=0):
    return render_template(
            'teacher/startAnswer.html', teacher_id=teacher_id
            )


@teacher_bp.route('/recordAnswer', methods=['GET', 'POST'])
def recordAnswer(teacher_id=0):
    answer_record = AnswerRecord()
    answer_A = answer_record.query.filter_by(choice1=1).count()
    answer_B = answer_record.query.filter_by(choice2=1).count()
    answer_C = answer_record.query.filter_by(choice3=1).count()
    answer_D = answer_record.query.filter_by(choice4=1).count()
    return jsonify({
        'A': answer_A,
        'B': answer_B,
        'C': answer_C,
        'D': answer_D
        })


@teacher_bp.route('/generateQR')
def generateQR(teacher_id=0):
    return "generateQR"


@teacher_bp.route('/questionSelect')
def questionSelect(teacher_id=0):
    return "questionSelect"


def redirect_url(default='teacher.addSubject'):
    return request.args.get('next') or \
           request.referrer or \
           url_for(default, teacher_id=current_user.id)
