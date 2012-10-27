#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model import *
from sqlalchemy.orm.exc import NoResultFound

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
                auth_token = AuthToken.uuid_token(self.db)
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
                auth_token = AuthToken.uuid_token(self.db)
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
        #already sign out
        return True

    def get_user_id(self, auth_token):
        try:
            token = self.db.query(AuthToken).filter(AuthToken.auth_token==auth_token).one()
        except NoResultFound:
            token = None
        if token is not None:
            return token.user_id
        return None

    def get_lessontables(self, auth_token):
        user_id = self.get_user_id(auth_token)
        if user_id is not None:
            try:
                lesson_tables = self.db.query(LessonTable).filter(LessonTable.user_id==user_id).all()
            except NoResultFound:
                lesson_tables = []
        else:
            #TODO Permission Error
            lesson_tables = []
        return lesson_tables

    def create_lessontable(self, auth_token):
        user_id = self.get_user_id(auth_token)
        print user_id
        if user_id is not None:
            lesson_table = LessonTable(user_id=user_id)
            self.db.add(lesson_table)
            return True
        else:
            return False

    def get_lessoninfos(self, lesson_table_id):
        try:
            lesson_table_items = self.db.query(LessonTableItem).filter(LessonTableItem.table_id==lesson_table_id).all()
        except NoResultFound:
            lesson_table_items = []
        lesson_infos = []
        for item in lesson_table_items:
            #TODO will item.lesson_info be null?
            lesson_infos.append(item.lesson_info)
        return lesson_infos

    def dept_provinces(self):
        try:
            provinces = self.db.query(Dept.province).group_by(Dept.province).all()
        except NoResultFound:
            provinces = []
        return provinces

    def add_obj(self, obj):
        self.db.add(obj)
