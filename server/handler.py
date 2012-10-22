#!/usr/bin/env python
# -*- coding: utf-8 -*-

# implate thrift service api
import sys
sys.path.append('../gen-py')
import model
from type.ttypes import *

class ClassNoteHandler:
    def __init__(self, ctrl):
        self.log = {}
        self.ctrl = ctrl

    def login_by_email(self, email, password):
        token = self.ctrl.login_by_email(email, password)
        if token is not None:
            return AuthResponse(auth_token = token.auth_token, expire_in = None, user_id = token.user_id) 
        return AuthResponse(auth_token = None, expire_in = None, user_id = None)

    def login_by_username(self, username, password):
        token = self.ctrl.login_by_username(username, password)
        if token is not None:
            return AuthResponse(auth_token = token.auth_token, expire_in = None, user_id = token.user_id) 
        return  AuthResponse(auth_token = None, expire_in = None, user_id = None)

    def sign_up_email(self, email, password):
        return self.ctrl.sign_up_email(email, password)

    def sign_up_username(self, username, password):
        return self.ctrl.sign_up_username(username, password)

    def sign_out(self, auth_token):
        return self.ctrl.sign_out(auth_token)

    def user_get(self, auth_token, user_id):
        pass

    def lessontable_get(self, auth_token, user_id):
        pass

    def lessontable_set(self, auth_token, user_id, lesson_tables):
        pass

    def course_add(self, course):
        if course.for_class is not None:
            model_course = model.Course(name = course.name, tearcher = course.teacher, book = course.book)
        pass

    def course_set(self, course):
        pass
