import time
from app.blueprints import teacher_bp
from flask import url_for, jsonify
from flask import redirect
from flask import g
from flask import flash
from flask import render_template
from flask import request
from flask_login import login_user, login_required, current_user
from app.forms import AddClasses
from app.forms import AddSubjectForm
from app.forms import AddChapterForm
from app.forms import AddExamPaper
from app.forms import AddQuestionForm
from app.forms import questionAnswerForm
from app.forms import ExamPaperToClasses
from app.models import Subject
from app.models import Classes
from app.models import UserInfo
from app.models import Teacher
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
        '/addClasses',
        methods=['GET', 'POST']
    )
def teacherIndex(teacher_id=0):
    from app.models import db
    form = AddClasses(teacher_id)
    if form.validate_on_submit():

        if Classes.query.filter_by(classes_id=form.classes_id.data).first():
            flash('该教学班已存在')
        else:
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
    else:
        flash("请检查是否科目信息不完整")
    return render_template('teacher/addClasses.html', form=form, redirect_url=redirect_url)


@teacher_bp.route('/showClasses', methods=['GET', 'POST'])
def showClasses(teacher_id=0):
    classes = Classes.query.filter_by(teacher_id=teacher_id).all()
    length = len(classes)
    return render_template(
            'teacher/showClasses.html', classes=classes, length=length,
            zip=zip, Subject=Subject
            )


@teacher_bp.route('/addSubject', methods=['GET', 'POST'])
def addSubject(teacher_id=0):
    from app.models import db
    subject = Teacher.query.get(teacher_id).subjects
    subject_name = []
    if subject:
        for i in subject:
            subject_name.append(i.subjectName)
    form = AddSubjectForm()
    if form.validate_on_submit():
        data = form.subject.data
        if data in subject_name:
            flash('科目已存在')
        else:
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


@teacher_bp.route('/showSubject', methods=["GET", "POST"])
def showSubject(teacher_id=0):
    subjects = Subject.query.filter_by(teacher_id=teacher_id).all()
    length = len(subjects)
    return render_template(
            "teacher/showSubject.html",
            teacher_id=teacher_id,
            subjects=subjects,
            length=length,
            zip=zip
            )


@teacher_bp.route('/subjectDelete/<int:subject_id>', methods=['GET', 'POST'])
def subjectDelete(subject_id=0, teacher_id=0):
    from app.models import db
    subject = Subject.query.get(subject_id)
    db.session.delete(subject)
    db.session.commit()
    return redirect(redirect_url())


@teacher_bp.route('/addChapter/<int:subject_id>', methods=['GET', 'POST'])
def addChapter(subject_id=0, teacher_id=0):
    from app.models import db
    subject = Subject.query.get(subject_id)
    form = AddChapterForm()
    chap = Subject.query.get(subject_id).chapters
    chap_name = []
    if chap:
        for i in chap:
            chap_name.append(i.chapterName)
    chapter = Chapter.query.filter_by(subject_id=subject_id).all()
    length = len(chapter)
    if form.validate_on_submit():
        data = form.chapter.data
        if data in chap_name:
            flash('章节名已存在')
        else:
            chapter = Chapter(chapterName=data)
            subject = Subject.query.get(subject_id)
            chapter.subject = subject
            db.session.add(chapter)
            db.session.commit()
            flash('添加成功')
            return redirect(url_for('teacher.showChapter', teacher_id=teacher_id, subject_id=subject_id))
    return render_template(
            'teacher/addChapter.html',
            form=form, chapter=chapter, teacher_id=teacher_id,
            length=length, zip=zip, subject=subject
            )


@teacher_bp.route('/showChapter/<int:subject_id>', methods=["GET", "POST"])
def showChapter(teacher_id=0, subject_id=0):
    subject = Subject.query.get(subject_id)
    chapters = subject.chapters
    length = len(chapters)
    return render_template(
            "teacher/showChapter.html",
            teacher_id=teacher_id,
            subject=subject,
            chapters=chapters,
            length=length,
            zip=zip
            )


@teacher_bp.route('/chapterDelete/<int:chapter_id>', methods=['GET', 'POST'])
def chapterDelete(chapter_id=0, teacher_id=0):
    from app.models import db
    chapter = Chapter.query.get(chapter_id)
    db.session.delete(chapter)
    db.session.commit()
    return redirect(redirect_url())

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


@teacher_bp.route('/showQues', methods=['GET', 'POST'])
def showQues(teacher_id=0):
    from app.models import db
    teacher = Teacher.query.get(teacher_id)
    questions = teacher.questions
    ques = Question.query.filter_by(teacher_id=teacher_id)
    subjects = Subject.query.filter_by(teacher_id=teacher_id).all()
    if subjects:
        chapters = "-1"
    else:
        chapters = 0
    if request.method == 'POST':
        chapter_id = request.form['ques_chapter']
        subject_id = request.form['ques_subject']
        ques_type = request.form['ques_type']
        ques_difficulty_start = request.form['ques_difficulty_start']
        ques_difficulty_end = request.form['ques_difficulty_end']
        ques = ques.filter(
                Question.difficulity >= ques_difficulty_start,
                Question.difficulity <= ques_difficulty_end
                )
        if ques_type == "mutiple":
            ques = ques.filter_by(type="选择题")
        elif ques_type == "fill":
            ques = ques.filter_by(type="填空题")
        if subject_id == " " or chapter_id == " ":
            flash("你需要先去创建完整的科目信息")
        elif subject_id == "-1":  # 科目为所有时
            chapters = "-1"
            questions = ques.all()
        elif chapter_id == "-1":  # 科目已选，章节为所有时
            questions = ques.filter_by(subject_id=subject_id)
        else:  # 科目章节均已选定
            questions = ques.filter(
                    Question.chapters.any(Chapter.id == chapter_id)
                    ).all()
    length = len(questions)
    return render_template(
        'teacher/showQues.html',
        questions=questions,
        length=length, zip=zip,
        teacher_id=teacher_id,
        subjects=subjects,
        chapters=chapters
    )


@teacher_bp.route('/addExamPaper/<int:chapter_id>', methods=['GET', 'POST'])
def addExamPaper(chapter_id=0, teacher_id=0):
    from app.models import db
    form = AddExamPaper()
    classes_exampaper = ExamPaperToClasses()
    teacher = Teacher().query.filter_by(teacher_id=teacher_id).first()
    classes = teacher.classes
    classes_exampaper.classes_select.choices += [(r.classes_id, r.classes_id) for r in classes]
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
            classes_exampaper=classes_exampaper,
            chapter_id=chapter_id,
            length=length, zip=zip, teacher_id=teacher_id
        )


@teacher_bp.route('/testExamPaper', methods=['GET', 'POST'])
def testExamPaper(teacher_id=0):
    from app.models import db
    exams = Teacher.query.get(teacher_id).exampapers
    exam_name = []
    if exams:
        for i in exams:
            exam_name.append(i.name)
    subjects = Subject.query.filter_by(teacher_id=teacher_id).all()
    if subjects:
        chapters = subjects[0].chapters
    else:
        chapters = 0
    if request.method == 'POST':
        chapter_id = request.form['exampaper_chapter']
        name = request.form['exampaper_name']
        if name in exam_name:
            flash('试卷名称已经存在，请重新输入')
        elif chapter_id == " ":
            flash("你需要先去创建完整的科目信息")
        else:
            exampaper = ExamPaper(
                    name=request.form['exampaper_name'],
                    subject_id=request.form['exampaper_subject'],
                    chapter_id=request.form['exampaper_chapter'],
                    teacher_id=teacher_id,
                    tag=request.form['exampaper_tag']
                    )
            db.session.add(exampaper)
            db.session.commit()
    return render_template(
            '/teacher/testExamPaper.html',
            subjects=subjects,
            chapters=chapters,
            teacher_id=teacher_id
        )


@teacher_bp.route('/listExamPaper')
def listExamPaper(teacher_id=0):
    classes_exampaper = ExamPaperToClasses()
    teacher = Teacher().query.filter_by(teacher_id=teacher_id).first()
    classes = teacher.classes
    classes_exampaper.classes_select.choices += [(r.id, r.classes_id) for r in classes]
    exampapers = teacher.exampapers
    length = len(exampapers)
    return render_template(
            'teacher/listExamPaper.html',
            teacher_id=teacher_id,
            exampapers=exampapers,
            classes_exampaper=classes_exampaper,
            length=length,
            zip=zip
            )


@teacher_bp.route('/addQues', methods=['GET', 'POST'])
def addQues(teacher_id=0):
    from app.models import db
    subjects = Subject.query.filter_by(teacher_id=teacher_id).all()
    if subjects:
        chapters = subjects[0].chapters
    else:
        chapters = 0
    if request.method == "POST":
        chapter_id = request.form['question_chapter']
        subject_id = request.form['question_subject']
        questionText = request.form['questionText']
        if Question.query.filter_by(questionText=questionText).first():
            flash('问题已经存在，请重新输入')
        elif chapter_id == " " or subject_id == " ":
            flash("请先去创建完整的科目信息")
        else:
            chapter = Chapter.query.get(chapter_id)
            question = Question(
                questionText=request.form['questionText'],
                difficulity=request.form['difficulty'],
                subject_id=subject_id,
                type=request.form.get('select'),
                teacher_id=teacher_id
            )
            question.chapters.append(chapter)
            type = request.form.get('select')
            if type == "选择题":
                mutipleChoice = MutipleChoice(
                    choice1=request.form['choice1'],
                    choice2=request.form['choice2'],
                    choice3=request.form['choice3'],
                    choice4=request.form['choice4'],
                    answer=request.form['answer']
                )
                question.mutipleChoice = mutipleChoice
                db.session.add(question)
            elif type == "填空题":
                fillInTheBlank = FillInTheBlanks(answer=request.form['answer'])
                question.fillInTheBlanks = fillInTheBlank
                db.session.add(question)
            db.session.commit()
            flash('提交成功')
    return render_template(
            'teacher/addQues.html',
            subjects=subjects,
            chapters=chapters,
            teacher_id=teacher_id
            )


@teacher_bp.route('/returnChapter/<int:subject_id>', methods=['GET', 'POST'])
def returnChapter(teacher_id=0, subject_id=0):
    print(type(subject_id))
    if subject_id != -1:
        subject = Subject.query.filter_by(id=subject_id).first()
        print(subject)
        chapters = subject.chapters
        print(chapters)
        if chapters:
            return jsonify([i.serialize() for i in chapters])
        else:
            return "0"
    else:
        return "-1"



@teacher_bp.route('/returnQues/<int:chapter_id>', methods=['GET', 'POST'])
def returnQues(teacher_id=0, chapter_id=0):
    chapter = Chapter.query.filter_by(id=chapter_id).first()
    questions = chapter.questions
    if questions:
        return jsonify([i.serialize() for i in questions])
    else:
        return {'1': 'null'}


@teacher_bp.route(
        '/exampaperToClasses/<int:exampaper_id>', methods=['POST']
        )
def exampaperToClasses(teacher_id=0, exampaper_id=0):
    from app.models import db
    form = ExamPaperToClasses()
    exampaper = ExamPaper().query.get(exampaper_id)
    classes_id = form.classes_select.data
    classes = Classes().query.get(classes_id)
    exampaper.classes.append(classes)
    db.session.add(exampaper)
    db.session.commit()
    flash('发布成功')
    classes_id = str(classes_id)
    exampaper_id = str(exampaper_id)
    return render_template(
            "teacher/generateQR.html",
            class_id=classes_id,
            exampaper_id=exampaper_id
            )


@teacher_bp.route(
        '/selectClasses', methods=['GET', 'POST']
        )
def selectClasses(teacher_id=0):
    teacher = Teacher().query.filter_by(teacher_id=teacher_id).first()
    classes = teacher.classes
    return jsonify([i.serialize() for i in classes])


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
        '/addQuesToExamPaper/<int:exampaper_id>',
        methods=['GET', 'POST']
        )
def addQuesToExamPaper(
        exampaper_id=0, teacher_id=0
        ):
    teacher = Teacher.query.get(teacher_id)
    exampaper = ExamPaper.query.filter_by(id=exampaper_id).first()
    questions = teacher.questions #是否需要传值得考量
    length = len(questions)
    return render_template(
        'teacher/addQuesToExamPaper.html',
        questions=questions,
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
    if form.validate_on_submit():
        question = Question(
            questionText=form.questionText.data,
            difficulity=form.difficulity.data,
            type=request.form.get('select')
        )
        question.chapters.append(chapter)
        type = request.form.get('select')
        if type == "选择题":
            mutipleChoice = MutipleChoice(
                choice1=form.choice1.data,
                choice2=form.choice2.data,
                choice3=form.choice3.data,
                choice4=form.choice4.data,
                answer=form.answer.data
            )
            question.mutipleChoice = mutipleChoice
            db.session.add(question)
        elif type == "填空题":
            fillInTheBlank = FillInTheBlanks(answer=form.answer.data)
            question.fillInTheBlanks = fillInTheBlank
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
    timestamp = int(time.time())
    timestamp = str(timestamp)
    return render_template(
            'teacher/startAnswer.html',
            teacher_id=teacher_id,
            timestamp=timestamp
            )


@teacher_bp.route('/deleteRecord', methods=['GET', 'POST'])
def deleteRecord(teacher_id=0):
    from app.models import db
    record = AnswerRecord()
    records = record.query.all()
    for record_item in records:
        db.session.delete(record_item)
    db.session.commit() 
    flash('数据清除完成')
    return redirect(redirect_url())


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
