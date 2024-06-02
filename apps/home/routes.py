# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from apps.home import blueprint
from flask import render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound
from apps.authentication.models import Users

@blueprint.route('/index')
def index():
    return render_template('home/index.html', segment='index')

@blueprint.route('/profile')
@login_required
def profile():
    return render_template('home/profile.html', user=current_user)

@blueprint.route('/update_username', methods=['POST'])
@login_required
def update_username():
    new_username = request.form['username']
    if new_username:
        user_id = current_user.id
        if Users.updateName(user_id, username=new_username):
            flash('Username updated successfully!', 'success')
        else:
            flash('Failed to update username.', 'danger')
    return redirect(url_for('home_blueprint.profile'))

@blueprint.route('/update_email', methods=['POST'])
@login_required
def update_email():
    new_email = request.form['email']
    if new_email:
        user_id = current_user.id
        if Users.updateEmail(user_id, email=new_email):
            flash('Email updated successfully!', 'success')
        else:
            flash('Failed to update email.', 'danger')
    return redirect(url_for('home_blueprint.profile'))

@blueprint.route('/update_password', methods=['POST'])
@login_required
def update_password():
    old_password = request.form['old_password']
    new_password = request.form['new_password']
    
    if old_password and new_password:
        user = current_user
        if Users.update_password(user, old_password, new_password):
            flash('Password updated successfully!', 'success')
        else:
            flash('Old password is incorrect.', 'danger')
    
    return redirect(url_for('home_blueprint.profile'))

@blueprint.route('/<template>')
@login_required
def route_template(template):
    try:
        if not template.endswith('.html'):
            template += '.html'
        segment = get_segment(request)
        return render_template("home/" + template, segment=segment)
    except TemplateNotFound:
        return render_template('home/page-404.html'), 404
    except:
        return render_template('home/page-500.html'), 500

def get_segment(request):
    try:
        segment = request.path.split('/')[-1]
        if segment == '':
            segment = 'index'
        return segment
    except:
        return None
