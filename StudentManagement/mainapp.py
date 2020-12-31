from flask import Flask, flash, jsonify, redirect, render_template, request, session
from StudentManagement import app, db
from StudentManagement.helpers import login_required
from StudentManagement.models import Account
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
                flash('Welcome')
                return render_template("/base/Error.html")
        else:
            flash(request.form.get("username"))
            return render_template("/base/Error.html")
        # Remember which user has logged in
        session["user_id"] = account.id

        # flask notice message
        flash('Welcome')

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



if __name__ == '__main__':
    from StudentManagement.admin_module import *
    app.run()
