from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_login import logout_user, login_user
from passlib.hash import pbkdf2_sha256 as hasher
from flask import flash, url_for, redirect, request, render_template, session
from views.users import get_user


class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


def login_page():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.data["username"]
            user = get_user(username)
            if user is not None:
                password = form.data["password"]
                if hasher.verify(password, user.password):
                    login_user(user, remember=True)
                    session["token"] = user.password
                    flash("You have logged in.")
                    next_page = request.args.get("next", url_for("home_page"))
                    return redirect(next_page)
            flash("Invalid credentials.")
    return render_template("login.html", form=form)


def logout_page():
    if request.method == "GET":
        logout_user()
        flash("You have logged out.")
        return redirect(url_for("home_page"))
