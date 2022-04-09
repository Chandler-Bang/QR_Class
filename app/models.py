from app import db
from app import login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def user_load(id):
    return UserInfo.query.get(int(id))


roles_permissions = db.Table(
        'roles_permissions',
        db.Column("role_id", db.Integer, db.ForeignKey('role.id')),
        db.Column("permission_id", db.Integer, db.ForeignKey('permission.id'))
        )


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    users = db.relationship("UserInfo", back_populates="role")
    permissions = db.relationship(
            'Permission', secondary=roles_permissions, back_populates="roles"
            )

    @staticmethod
    def init_role():
        from app import db
        roles_permissions_map = {
                'teacher': ['edit'],
                'student': ['add']
                }
        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            for permission_name in roles_permissions_map[role_name]:
                permission = \
                    Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    roles = db.relationship(
            'Role', secondary=roles_permissions, back_populates="permissions"
            )


class UserInfo(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    password_hash = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship("Role", back_populates="users")
    teachers = db.relationship('Teacher', back_populates="user")
    students = db.relationship('Student', back_populates="user")

    def generate_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_teacher(self):
        return self.role.name == 'teacher'

    def is_student(self):
        return self.role.name == 'student'


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teacher_id = db.Column(db.Integer, db.ForeignKey('user_info.id'))
    user = db.relationship('UserInfo', back_populates='teachers')
    # 老师和班级是一对多
    classes = db.relationship('Classes')
    # 老师和学科是一对多
    subjects = db.relationship('Subject')


class Subject(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    subjectName = db.Column(db.String(10), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    # 学科和班级一对多
    classes = db.relationship('Classes')
    chapters = db.relationship('Chapter', back_populates="subject")


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
    classes_id = db.Column(db.String(20), unique=True)
    terms = db.Column(db.String(20))
    studentCount = db.Column(db.Integer)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    grade = db.relationship('StudentGrade', back_populates='classes')
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
    classes_id = db.Column(db.Integer, db.ForeignKey('classes.id'))
    exampaper_id = db.Column(db.Integer, db.ForeignKey('exam_paper.id'))
    # 成绩和学生、试卷是一对多
    classes = db.relationship('Classes', back_populates='grade')
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
    exampapers = db.relationship("ExamPaper", back_populates="chapters")
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
    name = db.Column(db.String(120))
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id'))
    tag = db.Column(db.String(120))
    chapters = db.relationship("Chapter", back_populates="exampapers")
    questions = db.relationship(
        'Question', secondary=exampaper_question, back_populates='exampapers'
    )
    grade = db.relationship('StudentGrade', back_populates="exampapers")


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    questionText = db.Column(db.Text(254), nullable=False)
    difficulity = db.Column(db.Float(2), nullable=False)
    exampapers = db.relationship(
        'ExamPaper', secondary=exampaper_question, back_populates='questions'
    )
    type = db.Column(db.String(10), index=True, nullable=False)
    chapters = db.relationship(
        'Chapter', secondary=chapter_question, back_populates='questions'
    )
    mutipleChoice = db.relationship(
            'MutipleChoice', cascade="delete", uselist=False
            )
    fillInTheBlanks = db.relationship(
            'FillInTheBlanks', cascade="all", uselist=False
            )


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


class AnswerRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    choice1 = db.Column(db.String, default='0')
    choice2 = db.Column(db.String, default='0')
    choice3 = db.Column(db.String, default='0')
    choice4 = db.Column(db.String, default='0')
