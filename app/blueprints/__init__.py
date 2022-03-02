from flask import Blueprint


teacher_bp = Blueprint('teacher', __name__)
student_bp = Blueprint('student', __name__)
auth_bp = Blueprint('auth', __name__)


from app.blueprints import auth, student, teacher
