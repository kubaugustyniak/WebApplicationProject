from flask import render_template, request, flash, url_for,redirect
from ..models import User
from.forms import LoginForm, RegistrationForm
from flask_login import login_user, logout_user, login_required
from . import auth
from app import db

@auth.route('/login', methods=['GET','POST'])
def login():            #logging user
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # if everything is ok it redirect to index.html, as logged user
        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password')
    return render_template('login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():         #it register user
    form=RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    first_name=form.first_name.data,
                    last_name=form.last_name.data,
                    password=form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('You are registered!')
        return redirect(url_for('auth.login'))
    return render_template('register.html',form=form)