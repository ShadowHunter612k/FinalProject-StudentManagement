from flask import Flask, flash, jsonify, redirect, render_template, request, session
from StudentManagement import app, db
from StudentManagement.helpers import login_required
from StudentManagement.models import *
from werkzeug.security import check_password_hash, generate_password_hash


@app.route("/")
@login_required
def index():
    return render_template("/TeachingManager/index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("/base/Error.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("/base/Error.html")

        # Query database for username
        account = db.session.query(Account).filter(Account.username == request.form.get("username")).first()
        # Ensure username exists and password is correct
        if account:
            if not check_password_hash(account.password, request.form.get("password")):
                return render_template("/base/Error.html")
        else:
            return render_template("/base/Error.html")

        # Remember which user has logged in
        session["user_id"] = account.id
        session["username"] = account.username
        # flask notice message
        flash('Welcome ' + account.username)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("base/login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/generalregulations")
@login_required
def generalRegulations():
    """trang quản lý các quy định chung"""
    # lấy các quy định
    regulations = Regulations.query.all()
    # lấy danh sách các khối
    grades = Grade.query.all()
    # lấy danh sách các lớp
    classes = Classes.query.all()

    # tạo 1 dict lưu số lượng lớp theo khối
    classes_by_grade = {}

    for grade in grades:
        count = 0
        for classs in classes:
            if grade.grade_id == classs.grade:
                count += 1
                classes_by_grade[grade.name] = count

    return render_template("TeachingManager/general regulations.html", regulations=regulations[0], grades=grades,
                           classes=classes, listcount=classes_by_grade)


@app.route("/updateregulation/age", methods=["POST"])
def updateAgeRegulation():
    """thay đổi quy định về độ tuổi"""
    new_min_age = request.form.get("min-age")
    new_max_age = request.form.get("max-age")
    regulation = Regulations.query.first()
    regulation.min_age = new_min_age
    regulation.max_age = new_max_age
    db.session.commit()

    # flask notice message
    flash('Quy định về độ tuổi đã được thay đổi')
    return redirect("/generalregulations")


@app.route("/updateregulation/numclass", methods=["POST"])
def updateNumClassRegulation():
    """thay đổi quy định về số lượng lớp """
    new_max_class = request.form.get("max-classes")
    regulation = Regulations.query.first()
    regulation.num_of_classes = new_max_class
    db.session.commit()

    # flask notice message
    flash('Quy định về số lượng lớp đã được thay đổi')
    return redirect("/generalregulations")


@app.route("/updateregulation/maxstudents", methods=["POST"])
def updateNumOfStudentRegulation():
    """thay đổi quy định về sĩ số tối đa """
    new_max_students = request.form.get("max-students")
    regulation = Regulations.query.first()
    regulation.max_students = new_max_students
    db.session.commit()

    # flask notice message
    flash('Quy định về sĩ số đã được thay đổi')
    return redirect("/generalregulations")


@app.route("/updateregulation/classname", methods=["POST"])
def updateClassNameRegulation():
    """thay đổi quy định về tên lớp tối đa """
    new_class_name = request.form.get("classname")
    class_id = request.form.get("class-id")
    _class_ = Classes.query.filter_by(class_id=class_id).first()
    old_class_name = _class_.name
    _class_.name = new_class_name
    db.session.commit()

    # flask notice message
    flash('Lớp '+old_class_name+' đã được đổi tên thành '+new_class_name)
    return redirect("/generalregulations")

@app.route("/educationregulations")
@login_required
def educationRegulation():
    """trang quản lý các quy định về học tập"""
    # lấy các quy định
    regulations = Regulations.query.all()
    # lấy danh sách các môn học
    subjects = Subjects.query.all()

    return render_template("TeachingManager/education regulations.html", regulations=regulations[0],subjects=subjects)


@app.route("/updateregulation/numofsubjects", methods=["POST"])
def updateNumOfSubjectRegulation():
    """thay đổi quy định về độ số lượng môn học"""
    new_numofsubjects = request.form.get("numofsubjects")
    regulation = Regulations.query.first()
    regulation.num_of_subjects = new_numofsubjects
    db.session.commit()

    # flask notice message
    flash('Quy định về số lượng môn học đã được thay đổi')
    return redirect("/educationregulations")


@app.route("/updateregulation/passgrade", methods=["POST"])
def updatePassGradeRegulation():
    """thay đổi quy định về điểm chuẩn đạt môn"""
    new_passgrade = request.form.get("passgrade")
    regulation = Regulations.query.first()
    regulation.pass_grade = new_passgrade
    db.session.commit()

    # flask notice message
    flash('Quy định về điểm chuẩn đã được thay đổi')
    return redirect("/educationregulations")


@app.route("/updateregulation/subjectname", methods=["POST"])
def updateSubjectNameRegulation():
    """thay đổi quy định về tên môn học """
    new_subject_name = request.form.get("subject-name")
    subject_id = request.form.get("subject-id")
    subject = Subjects.query.filter_by(subject_id=subject_id).first()
    old_subject_name = subject.name
    subject.name = new_subject_name
    db.session.commit()

    # flask notice message
    flash('Môn học '+old_subject_name+' đã được đổi tên thành '+new_subject_name)
    return redirect("/educationregulations")



if __name__ == '__main__':
    from StudentManagement.admin_module import *

    app.run()
