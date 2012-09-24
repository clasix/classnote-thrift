#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model import User, AuthToken
from sqlalchemy.orm.exc import NoResultFound

AUTH_TOKEN_LENGTH = 20

class Ctrl(object):
    """
    Use to control the auth model
    """

    def __init__(self, db=None):
       # FIXME if db is None, then ?
       self.db = db
    
    def login_by_email(self, email, password):
        try:
            user = self.db.query(User).filter(User.email==email).one()
        except NoResultFound:
            user = None
        if user is not None:
            if user.authenticate(password):
                auth_token = AuthToken.uuid_token(db)
                token = AuthToken(user_id=user.id, auth_token=auth_token)
                self.db.add(token)
                return token
        print 'User not found with email: %s' % email
        return None

    def login_by_username(self, username, password):
        try:
            user = self.db.query(User).filter(User.username==username).one()
        except NoResultFound:
            user = None
        if user is not None:
            if user.authenticate(password):
                auth_token = AuthToken.uuid_token(db)
                token = AuthToken(user_id=user.id, auth_token=auth_token)
                self.db.add(token)
                return token
        return None


    def sign_up_email(self, email, password):
        if self.db.query(User).filter(User.email==email).first():
            return False # User already exists.
        user = User(email=email, password=password)
        self.db.add(user)
        return True

    def sign_up_username(self, username, password):
        if self.db.query(User).filter(User.username==username).first():
            return False # User already exists.
        user = User(username=username, password=password)
        self.db.add(user)
        return True


    def sign_out(self, auth_token):
        try:
            token = self.db.query(AuthToken).filter(AuthToken.auth_token==auth_token).one()
        except NoResultFound:
            token = None
        if token is not None:
            self.db.delete(token)
            return True
        return False #already sign out

    def add_obj(self, obj):
        self.db.add(obj)

    // how to filter by cls and an object of the cls?
    def has_Class(self, a_class):
        try:
           the_class = self.db.query(Class).filter(Class.schoole == a_class.school, Class.dept == a_class.dept, Class.major = a_class.major, Class.year = a_Class.year) 

