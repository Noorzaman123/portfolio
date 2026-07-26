"""Auth routes: login and logout."""
from datetime import datetime
from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import auth_bp
from ...models.user import User


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        remember = bool(request.form.get('remember_me'))

        user = User.query.filter_by(username=username).first()

        if user and user.check_password(password):
            user.last_login = datetime.utcnow()
            from ...extensions import db
            db.session.commit()
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            flash('Welcome back, ' + user.username + '!', 'success')
            return redirect(next_page or url_for('admin.dashboard'))
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))
