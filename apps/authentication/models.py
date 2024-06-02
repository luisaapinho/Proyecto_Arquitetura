# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from flask_login import UserMixin
from apps import db, login_manager
from apps.authentication.util import hash_pass, verify_pass

class Users(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, **kwargs):
        for property, value in kwargs.items():
            if hasattr(value, '__iter__') and not isinstance(value, str):
                value = value[0]

            if property == 'password':
                value = hash_pass(value)  # Ensure the password is hashed

            setattr(self, property, value)

    def __repr__(self):
        return str(self.username)

    @staticmethod
    def updateName(id, username=None):
        user = Users.query.get(id)
        if user:
            if username:
                user.username = username
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def updateEmail(id, email=None):
        user = Users.query.get(id)
        if user:
            if email:
                user.email = email
            db.session.commit()
            return True
        return False
    
    @staticmethod
    def update_password(self, old_password, new_password):
        if verify_pass(old_password, self.password):
            self.password = hash_pass(new_password)
            db.session.commit()
            return True
        return False

    @login_manager.user_loader
    def user_loader(id):
        return Users.query.get(int(id))

    @login_manager.request_loader
    def request_loader(request):
        username = request.form.get('username')
        user = Users.query.filter_by(username=username).first()
        return user if user else None
