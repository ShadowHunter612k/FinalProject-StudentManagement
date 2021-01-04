from flask import Flask, flash, jsonify, redirect, render_template, request, session
from StudentManagement import app, db
from StudentManagement.helpers import login_required
from StudentManagement.models import *
from werkzeug.security import check_password_hash, generate_password_hash
import json


@app.route("/")
@login_required
def index():
    students = Students.query.all()
    teachers = Teachers.query.all()
    students = len(students)
    teachers = len(teachers)
    return render_template("/base/index.html", students=students, teachers=teachers)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash('Tên đăng nhập hoặc mật khẩu không hợp lệ!')
            return redirect("/")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash('Tên đăng nhập hoặc mật khẩu không hợp lệ!')
            return redirect("/")

        # Query database for username
        account = db.session.query(Account).filter(Account.username == request.form.get("username")).first()
        # Ensure username exists and password is correct
        if account:
            if not check_password_hash(account.password, request.form.get("password")):
                flash('Tên đăng nhập hoặc mật khẩu không hợp lệ!')
                return redirect("/")
        else:
            flash('Tên đăng nhập hoặc mật khẩu không hợp lệ!')
            return redirect("/")

        # Remember which user has logged in
        session["user_id"] = account.id
        session["username"] = account.username
        session["role"] = account.role
        # flask notice message
        flash('Welcome ' + account.username)

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("base/login.html")


@app.route("/logout")
@login_required
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

    # lọc số lượng lớp theo khối
    for grade in grades:
        count = 0
        for classs in classes:
            if grade.grade_id == classs.grade:
                count += 1
                classes_by_grade[grade.name] = count

    return render_template("TeachingManager/general regulations.html", regulations=regulations[0], grades=grades,
                           classes=classes, listcount=classes_by_grade)


@app.route("/updateregulation/age", methods=["POST"])
@login_required
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
@login_required
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
@login_required
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
@login_required
def updateClassNameRegulation():
    """thay đổi quy định về tên lớp tối đa """
    new_class_name = request.form.get("classname")
    class_id = request.form.get("class-id")
    _class_ = Classes.query.filter_by(class_id=class_id).first()
    old_class_name = _class_.name
    _class_.name = new_class_name
    db.session.commit()

    # flask notice message
    flash('Lớp ' + old_class_name + ' đã được đổi tên thành ' + new_class_name)
    return redirect("/generalregulations")


@app.route("/educationregulations")
@login_required
def educationRegulation():
    """trang quản lý các quy định về học tập"""
    # lấy các quy định
    regulations = Regulations.query.all()
    # lấy danh sách các môn học
    subjects = Subjects.query.all()

    return render_template("TeachingManager/education regulations.html", regulations=regulations[0], subjects=subjects)


@app.route("/updateregulation/numofsubjects", methods=["POST"])
@login_required
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
@login_required
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
@login_required
def updateSubjectNameRegulation():
    """thay đổi quy định về tên môn học """
    new_subject_name = request.form.get("subject-name")
    subject_id = request.form.get("subject-id")
    subject = Subjects.query.filter_by(subject_id=subject_id).first()
    old_subject_name = subject.name
    subject.name = new_subject_name
    db.session.commit()

    # flask notice message
    flash('Môn học ' + old_subject_name + ' đã được đổi tên thành ' + new_subject_name)
    return redirect("/educationregulations")


@app.route("/managestudent/addstudent", methods=["GET", "POST"])
@login_required
def addStudent():
    """Thêm tiếp nhận học sinh """

    if request.method == 'GET':
        # đi đến trang tiếp nhận học sinh
        return render_template("TeachingManager/add student.html")
    else:
        # lấy request thông tin học sinh
        firstname = request.form.get("firstname")
        lastname = request.form.get("lastname")
        gender = request.form.get("gender")
        email = request.form.get("email")
        birthdate = request.form.get("birthday")
        address = request.form.get("address")

        # thêm học sinh vào csdl
        student = Students(firstname=firstname, lastname=lastname, gender=gender, address=address, email=email,
                           birthdate=birthdate)
        db.session.add(student)
        db.session.commit()

        # flask notice message
        flash('HỌc sinh ' + lastname + ' ' + firstname + ' đã được tiếp nhận thành công!')
        return redirect("/managestudent/addstudent")


@app.route("/managestudent/searchstudent", methods=["GET", "POST"])
@login_required
def searchStudent():
    """tìm kiếm học sinh"""
    students = Students.query.all()
    return render_template("base/search student.html", students=students)


@app.route("/managestudent/sortstudent", methods=["GET", "POST"])
@login_required
def sortStudent():
    """xếp lớp cho học sinh"""
    # lấy danh sách các khối
    grades = Grade.query.all()
    # lấy danh sách các lớp
    classes = Classes.query.all()
    # danh sách học sinh cần xếp lớp khối 10
    unsorted10 = Students.query.filter_by(year_id=1, class_id=None)
    # danh sách học sinh cần xếp lớp khối 11
    unsorted11 = Students.query.filter_by(year_id=2, class_id=None)
    # danh sách học sinh cần xếp lớp khối 12
    unsorted12 = Students.query.filter_by(year_id=3, class_id=None)

    if request.method == 'GET':
        # danh sách học sinh
        students = Students.query.all()

        return render_template("TeachingManager/sort student.html", students=students, unsorted10=unsorted10,
                               unsorted11=unsorted11, unsorted12=unsorted12, grades=grades, classes=classes)
    else:
        # láy khối cần xếp lớp
        sort_grade = request.form.get('grade')
        student_list = []
        if sort_grade == '10':
            # lấy danh sách các lớp theo khối
            classes = Classes.query.filter_by(grade=1)
            student_list = unsorted10
        elif sort_grade == '11':
            # lấy danh sách các lớp theo khối
            classes = Classes.query.filter_by(grade=2)
            student_list = unsorted11
        else:
            # lấy danh sách các lớp theo khối
            classes = Classes.query.filter_by(grade=3)
            student_list = unsorted12
        print(classes)
        # xếp lớp cho các lớp theo khối
        num_class = classes.count()
        index = 0
        for student in student_list:
            if index <= num_class - 1:
                student.class_id = classes[index].class_id
                db.session.commit()
                index += 1
                if index == num_class:
                    index = 0

        # flask notice message
        flash('Hệ thống đã tự động xếp lớp cho khối ' + sort_grade)

        return redirect('/managestudent/sortstudent')


@app.route("/manageaccount/adduser", methods=["GET", "POST"])
@login_required
def addUser():
    """thêm user mới """
    if request.method == 'GET':
        return render_template("TeachingManager/add user.html")
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        role = request.form.get("role")

        account = Account(username=username, password=generate_password_hash(password), role=role, name=name)
        db.session.add(account)
        db.session.commit()

        # flask notice message
        flash('Tài khoản ' + username + ' đã được tạo thành công!')
        return redirect("/manageaccount/adduser")


@app.route("/managestudent/scoreinfo", methods=["GET", "POST"])
@login_required
def infoScore():
    """hiển thị thông tin nhập điểm"""
    if request.method == 'GET':
        # lấy thông tin giáo viên
        teacher = Teachers.query.filter_by(account_id=session["user_id"]).first()
        # lấy teacher_id
        teacher_id = teacher.teacher_id
        # lấy các lớp giáo viên được phân công dạy
        assignments = Assignments.query.filter_by(teacher_id=teacher_id)
        # lấy học kì
        semesters = Semesters.query.all()
        # lấy năm học
        school_years = School_year.query.all()

        return render_template("Teacher/score info.html", teacher=teacher, assignments=assignments, semesters=semesters,
                               school_years=school_years)
    else:
        # lấy loại điểm
        score_type = request.form.get('score_type')
        class_id = request.form.get('class_id')
        semester_id = request.form.get('semester_id')
        year_id = request.form.get('year_id')

        session['score_type'] = score_type
        session['class_id'] = class_id
        session['semester_id'] = semester_id
        session['year_id'] = year_id
        return redirect("/managestudent/addscore")


@app.route("/managestudent/addscore", methods=["GET", "POST"])
@login_required
def addScore():
    """hiển thị danh sách nhập điểm"""
    if request.method == 'GET':
        # lưu điểm mà giáo viên đã nhập
        session['temp'] = {}
        # lấy thông tin giáo viên
        teacher = Teachers.query.filter_by(account_id=session["user_id"]).first()
        # lấy teacher_id
        teacher_id = teacher.teacher_id
        # lấy id môn học
        subject_id = teacher.subject_id

        # lấy lớp cần nhập điểm
        class_ = Classes.query.filter_by(class_id=session["class_id"]).first()
        # lấy danh sách học sinh theo lớp
        students = Students.query.filter_by(class_id=session["class_id"]).all()

        # tạo bảng điểm của môn học
        for student in students:
            # kiểm tra học sinh có bảng điểm chưa
            check = ScoreBoard.query.filter_by(student_id=student.student_id, teacher_id=teacher_id,
                                               subject_id=subject_id, school_year_id=session['year_id'],
                                               semester_id=session['semester_id']).first()
            # nếu học sinh chưa có bảng điểm
            if check == None:
                # thêm bảng điểm vào csdl
                board = ScoreBoard(student_id=student.student_id, teacher_id=teacher_id, subject_id=subject_id,
                                   school_year_id=session['year_id'], semester_id=session['semester_id'])
                db.session.add(board)
                db.session.commit()

        # lấy thông tin bảng điểm
        score_board = ScoreBoard.query.filter_by(teacher_id=teacher_id, subject_id=subject_id,
                                                 school_year_id=session['year_id'],
                                                 semester_id=session['semester_id']).all()
        # lấy điểm theo loại
        scores = Score.query.filter_by(type_id=session['score_type'])
        # lấy loại điểm
        type = ScoreType.query.filter_by(type_id=session['score_type']).first()

        # for board in score_board:
        #     print(board.board_id)
        #     print(board.student_id)
        # for s in scores:
        #     print(s.board_id)
        return render_template("Teacher/add score.html", teacher=teacher, students=students, score_board=score_board,
                               scores=scores, class_=class_, type=type)
    else:
        # lưu điểm của học sinh
        score_list = session['temp']
        # print(score_list)
        for board_id, score_value in score_list.items():
            # print(board_id)
            # print(score_value)
            score = Score(score=score_value, type_id=session['score_type'], board_id=board_id)
            db.session.add(score)
            db.session.commit()
        # print(1)
        return redirect('/managestudent/addscore')


@app.route("/addscores/savetempscores", methods=["POST"])
@login_required
def saveTempScores():
    """lưu điểm mà giáo viên nhập"""
    score = request.form.get('score')
    board_id = request.form.get('board_id')
    print(score)
    print(board_id)
    temp = session['temp']
    temp[board_id] = score
    session['temp'] = temp
    print(session['temp'])
    return json.dumps({'status': 'OK'})


@app.route("/managestudent/classlist", methods=["GET"])
@login_required
def studentListByClass():
    """hiển thị danh sách học sinh theo lớp"""
    students = Students.query.filter_by(class_id=session['class_info']).all()
    count = len(students)
    return render_template("/base/students list.html", students=students, count=count)


@app.route("/managestudent/classinfo", methods=["GET", "POST"])
@login_required
def classInfo():
    """nhập thông tin lớp"""
    if request.method == 'GET':
        # lấy danh sách các lớp
        classes = Classes.query.all()
        return render_template("/base/class info.html", classes=classes)
    else:
        session['class_info'] = request.form.get('class_id')
        return redirect('/managestudent/classlist')


@app.route("/report/subjectscores", methods=["GET", "POST"])
@login_required
def subjectScores():
    """bảng điểm môn học cho giáo viên"""
    if request.method == 'GET':
        # lấy thông tin giáo viên
        teacher = Teachers.query.filter_by(account_id=session["user_id"]).first()
        # lấy teacher_id
        teacher_id = teacher.teacher_id
        # lấy các lớp giáo viên được phân công dạy
        assignments = Assignments.query.filter_by(teacher_id=teacher_id)
        # lấy học kì
        semesters = Semesters.query.all()
        # lấy năm học
        school_years = School_year.query.all()

        return render_template("Teacher/score board info.html", teacher=teacher, assignments=assignments,
                               semesters=semesters,
                               school_years=school_years)
    else:
        # lấy thông tin giáo viên
        teacher = Teachers.query.filter_by(account_id=session["user_id"]).first()
        # lấy teacher id
        teacher_id = teacher.teacher_id
        # lấy teacher id
        subject_id = teacher.subject_id
        # lấy lớp
        class_ = Classes.query.filter_by(class_id=request.form.get('class_id')).first()
        # lấy học sinh trong lớp
        students = Students.query.filter_by(class_id=request.form.get('class_id')).all()
        # lấy bảng điểm
        score_boards = ScoreBoard.query.filter_by(teacher_id=teacher_id, subject_id=subject_id,
                                                  school_year_id=request.form.get('year_id'),
                                                  semester_id=request.form.get('semester_id')).all()
        # lấy điểm
        scores = Score.query.all()
        return render_template("Teacher/subject score board.html", teacher=teacher, score_boards=score_boards,
                               students=students, class_=class_, scores=scores)


def average_score(student_id, year_id):
    """tính điểm trung bình học kì của học sinh """

    # lấy tất cả môn học
    subjects = Subjects.query.all()

    hk1_sum = 0
    count1 = 0
    hk2_sum = 0
    count2 = 0
    for subject in subjects:
        hk1_sum += avg_score(subject.subject_id, 1, year_id, student_id)
        count1 += 1
        hk2_sum += avg_score(subject.subject_id, 2, year_id, student_id)
        count2 += 1

    return [round(hk1_sum / count1, 1), round(hk2_sum / count2, 1)]


@app.route("/studentsmanager/studyresult", methods=["GET", "POST"])
@login_required
def study_result():
    """ kết quả học tập của học sinh"""
    if request.method == 'GET':
        # lấy năm học
        school_years = School_year.query.all()
        return render_template("/base/result info.html", school_years=school_years)
    else:
        # lấy danh sách học sinh
        students = Students.query.all()
        # tạo 1 dictionary chứa student_id và điểm
        students_scores = {}
        # expected {'1,[2,3]'}
        for student in students:
            students_scores[student.student_id] = average_score(student.student_id, request.form.get('semester_id',
                                                                                                     request.form.get(
                                                                                                         'year_id')))
        return render_template("/base/study result.html", students=students, students_scores=students_scores)


def num_of_students(class_id):
    """sĩ số theo lớp"""
    students = Students.query.filter_by(class_id=class_id).all()
    return len(students)


def pass_std_by_subject(subject_id, semester_id, year_id, class_id):
    '''số học sinh đạt môn'''
    # lấy học sinh theo lớp
    students = Students.query.filter_by(class_id=class_id)
    count = 0
    # lấy số học sinh đạt theo môn và học kì
    for student in students:
        if avg_score(subject_id, semester_id, year_id, student.student_id) >= 5:
            count += 1
    return count


def avg_score(subject_id, semester_id, year_id, student_id):
    """điểm trung bình môn theo học kì """
    # lấy bảng điểm theo môn
    board = ScoreBoard.query.filter_by(student_id=student_id, subject_id=subject_id, semester_id=semester_id,
                                       school_year_id=year_id).first()
    # nếu chưa có điểm thì trả về 0
    if board is None:
        return 0
    # lấy điểm theo bảng điểm
    scores = Score.query.filter_by(board_id=board.board_id).all()

    # tính điểm trung bình môn
    sum = 0
    count = 0
    # nếu chưa có điểm thì trả về 0
    if len(scores) == 0:
        return 0
    else:
        for score in scores:
            # điểm tb môn = điểm x hệ số
            sum += score.score * score.type_id
            count += score.type_id

    return round((sum / count), 2)


def pass_std(semester_id, year_id, class_id):
    """số học sinh đạt theo lớp"""
    # lấy học sinh theo lớp
    students = Students.query.filter_by(class_id=class_id)
    # lấy tất cả môn học
    subjects = Subjects.query.all()
    # số học sinh đạt
    count = 0
    # lấy số học sinh đạt theo môn và học kì
    for student in students:
        # tính điểm trung bình tát cả các môn
        sum_avg = 0
        count_subject = 0
        for subject in subjects:
            sum_avg += avg_score(subject.subject_id, semester_id, year_id, student.student_id)
            count_subject += 1
        if sum_avg / count_subject >= 5:
            count += 1
    return count


@app.route("/report/subjectsummary", methods=["GET", "POST"])
@login_required
def subjectSummary():
    """báo cáo tổng kết môn"""
    # lấy thông tin giáo viên
    teacher = Teachers.query.filter_by(account_id=session["user_id"]).first()
    if request.method == 'GET':
        # lấy năm học
        school_years = School_year.query.all()
        # lấy học kì
        semesters = Semesters.query.all()
        return render_template("/Teacher/report info.html", school_years=school_years, semesters=semesters,
                               teacher=teacher)
    else:
        # lấy lớp
        classes = Classes.query.all()
        # lấy môn học
        subject_id = teacher.subject_id
        # lấy học kì
        semester_id = request.form.get('semester_id')
        semester = Semesters.query.filter_by(semester_id=semester_id).first()
        # lấy năm học
        year_id = request.form.get('year_id')
        year = School_year.query.filter_by(year_id=year_id).first()
        # tạo dict đễ lưu thông tin
        class_info = {}
        # lấy thông tin theo từng lớp
        for class_ in classes:
            # sĩ số
            std_num = num_of_students(class_.class_id)
            # số lượng đat
            pass_num = pass_std_by_subject(subject_id, semester_id, year_id, class_.class_id)
            # tỉ lệ
            rate = round((pass_num / std_num) * 100, 1)
            class_info[class_.class_id] = [std_num, pass_num, rate]

        return render_template("/Teacher/subject summary.html", teacher=teacher, semester=semester, year=year,
                               class_info=class_info, classes=classes)


@app.route("/report/semestersummary", methods=["GET", "POST"])
@login_required
def semesterSummary():
    """báo cáo tổng kết học kì"""
    if request.method == 'GET':
        # lấy năm học
        school_years = School_year.query.all()
        # lấy học kì
        semesters = Semesters.query.all()
        return render_template("/TeachingManager/summary info.html", school_years=school_years, semesters=semesters)
    else:
        # lấy lớp
        classes = Classes.query.all()
        # lấy học kì
        semester_id = request.form.get('semester_id')
        semester = Semesters.query.filter_by(semester_id=semester_id).first()
        # lấy năm học
        year_id = request.form.get('year_id')
        year = School_year.query.filter_by(year_id=year_id).first()
        # tạo dict đễ lưu thông tin
        class_info = {}
        # lấy thông tin theo từng lớp
        for class_ in classes:
            # sĩ số
            std_num = num_of_students(class_.class_id)
            # số lượng đat
            pass_num = pass_std(semester_id, year_id, class_.class_id)
            # tỉ lệ
            rate = round((pass_num / std_num) * 100, 1)
            class_info[class_.class_id] = [std_num, pass_num, rate]

        return render_template("/TeachingManager/semester summary.html", semester=semester, year=year,
                               class_info=class_info, classes=classes)


if __name__ == '__main__':
    from StudentManagement.admin_module import *

    app.run()
