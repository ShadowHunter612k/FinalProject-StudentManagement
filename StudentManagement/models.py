from sqlalchemy import Column, Integer, Float, String, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from StudentManagement import db


class Account(db.Model):
    __tablename__ = 'account'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(Integer, nullable=False)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Grade(db.Model):
    __tablename__ = 'Grade'

    grade_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Classes(db.Model):
    __tablename__ = 'classes'

    class_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    grade = Column(Integer, ForeignKey(Grade.grade_id), nullable=False)
    grade_name = db.relationship('Grade', backref=db.backref('grade', lazy='dynamic'))

    def __str__(self):
        return self.name


class Students(db.Model):
    __tablename__ = 'students'

    student_id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    birthdate = Column(Date, nullable=False)
    class_id = Column(Integer, ForeignKey(Classes.class_id), nullable=True)
    class_name = db.relationship('Classes', backref=db.backref('class', lazy='dynamic'))

    def __str__(self):
        return  self.firstname +" " +self.lastname


class Regulations(db.Model):
    __tablename__ = 'regulations'

    re_id = Column(Integer, primary_key=True, autoincrement=True)
    min_age = Column(Integer)
    max_age = Column(Integer)
    max_students = Column(Integer)
    num_of_classes = Column(Integer)
    pass_grade = Column(Integer)
    num_of_subjects = Column(Integer)


class Subjects(db.Model):
    __tablename__ = 'subjects'

    subject_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name


class Semesters(db.Model):
    __tablename__ = 'semesters'

    semester_id = Column(Integer, primary_key=True, autoincrement=True)
    semester = Column(String(50), nullable=False)

    def __str__(self):
        return self.semester


class School_year(db.Model):
    __tablename__ = 'school_year'

    year_id = Column(Integer, primary_key=True, autoincrement=True)
    year = Column(String(50), nullable=False)

    def __str__(self):
        return self.year


class Teachers(db.Model):
    __tablename__ = 'teachers'

    teacher_id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(50), nullable=False)
    lastname = Column(String(50), nullable=False)
    gender = Column(String(10), nullable=False)
    address = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    birthdate = Column(Date, nullable=False)
    subject_id = Column(Integer, ForeignKey(Subjects.subject_id), nullable=False)
    subject = db.relationship('Subjects', backref=db.backref('teach', lazy='dynamic'))
    account_id = Column(Integer, ForeignKey(Account.id), nullable=False)
    account = db.relationship('Account', backref=db.backref('own', lazy='dynamic'))

    def __str__(self):
        return  self.firstname +" " +self.lastname

class Ftm_scores(db.Model):
    __tablename__ = 'ftm_scores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float, nullable=False)

    def __str__(self):
        return str(self.score)


class Stm_scores(db.Model):
    __tablename__ = 'stm_scores'

    id = Column(Integer, primary_key=True, autoincrement=True)
    score = Column(Float, nullable=False)

    def __str__(self):
        return str(self.score)


class Scores(db.Model):
    __tablename__ = 'scores'

    score_id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey(Students.student_id), nullable=False)
    student = db.relationship('Students', backref=db.backref('score', lazy='dynamic'))
    teacher_id = Column(Integer, ForeignKey(Teachers.teacher_id), nullable=False)
    teacher = db.relationship('Teachers', backref=db.backref('score', lazy='dynamic'))
    subject_id = Column(Integer, ForeignKey(Subjects.subject_id), nullable=False)
    subject = db.relationship('Subjects', backref=db.backref('score', lazy='dynamic'))
    school_year_id = Column(Integer, ForeignKey(School_year.year_id), nullable=False)
    school_year = db.relationship('School_year', backref=db.backref('score', lazy='dynamic'))
    semester_id = Column(Integer, ForeignKey(Semesters.semester_id), nullable=False)
    semester = db.relationship('Semesters', backref=db.backref('score', lazy='dynamic'))
    ftm_scores_id = Column(Integer, ForeignKey(Ftm_scores.id), nullable=False)
    ftm_scores = db.relationship('Ftm_scores', backref=db.backref('score_s', lazy='dynamic'))
    stm_scores_id = Column(Integer, ForeignKey(Stm_scores.id), nullable=False)
    stm_scores = db.relationship('Stm_scores', backref=db.backref('score_s', lazy='dynamic'))

    def __str__(self):
        return self.subject


if __name__ == '__main__':
    db.create_all()
