from flask import render_template, redirect, request, url_for
from flask_login import current_user, login_user, logout_user

from apps import db, login_manager
from apps.authentication import blueprint
from apps.authentication.forms import LoginForm, CreateAccountForm
from apps.authentication.models import Users
from apps.authentication.util import verify_pass

@blueprint.route('/')
def route_default():
    return redirect(url_for('home_blueprint.index'))

# Login & Registration

@blueprint.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and 'login' in request.form:
        # Read form data
        username = request.form['username']
        password = request.form['password']

        # Locate user
        user = Users.query.filter_by(username=username).first()

        # Check the password
        if user and verify_pass(password, user.password):
            login_user(user)
            return redirect(url_for('home_blueprint.index'))

        # Something (user or pass) is not ok
        return render_template('accounts/login.html',
                               msg='Wrong user or password',
                               form=login_form)

    if not current_user.is_authenticated:
        return render_template('accounts/login.html', form=login_form)
    return redirect(url_for('home_blueprint.index'))

@blueprint.route('/register', methods=['GET', 'POST'])
def register():
    create_account_form = CreateAccountForm(request.form)
    if request.method == 'POST' and 'register' in request.form:
        username = request.form['username']
        email = request.form['email']

        # Check if username exists
        user = Users.query.filter_by(username=username).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Username already registered',
                                   success=False,
                                   form=create_account_form)

        # Check if email exists
        user = Users.query.filter_by(email=email).first()
        if user:
            return render_template('accounts/register.html',
                                   msg='Email already registered',
                                   success=False,
                                   form=create_account_form)

        # Create the user
        user = Users(**request.form)
        db.session.add(user)
        db.session.commit()

        # Log out the user
        logout_user()

        return render_template('accounts/register.html',
                               msg='User created successfully.',
                               success=True,
                               form=create_account_form)

    return render_template('accounts/register.html', form=create_account_form)

@blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home_blueprint.index'))

# Errors

@login_manager.unauthorized_handler
def unauthorized_handler():
    login_form = LoginForm(request.form)
    if not current_user.is_authenticated:
        return render_template('accounts/login.html', msg='You need to be authenticated to access the cart', form=login_form)
    # Redirect to the cart page if the user is authenticated
    return redirect(url_for('home_blueprint.cart'))

@blueprint.errorhandler(403)
def access_forbidden(error):
    return render_template('home/page-403.html'), 403

@blueprint.errorhandler(404)
def not_found_error(error):
    return render_template('home/page-404.html'), 404

@blueprint.errorhandler(500)
def internal_error(error):
    return render_template('home/page-500.html'), 500
