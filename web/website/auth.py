from flask import Blueprint, render_template, request, flash, redirect, url_for
from .config import Config
from .forms import RegisterForm, LoginForm
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        print(f"\n[INFO] Form submitted to login!\n")
        user_input = User.query.filter_by(username=form.username.data).first()
        print(f"\nUSER INPUT : {user_input}\n", )
        if user_input and user_input.check_password(input_password=form.password.data):
            login_user(user_input)
            # login_user(user, remember=form.remember.data)
            flash(
                f"You are logged in! Welcome "
                f"{user_input.username}", category='success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('views.home'))
        else:
            flash('Wrong password! Please try again.', category='danger')
    return render_template('login.html', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        print(f"\n[INFO] Creating user ...\n")
        user_input = User(username=form.username.data,
                          password=form.password.data)
        db.session.add(user_input)
        db.session.commit()
        login_user(user_input)
        flash(
            f"Account created successfully! Welcome "
            f"{user_input.username}", category='success')
        return redirect(url_for('views.home'))
    return render_template('register.html', form=form)


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully!", category="primary")
    return redirect(url_for('views.home'))
