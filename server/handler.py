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

    def get_lessontables(self, auth_token):
        lesson_tables = self.ctrl.get_lessontables(auth_token)
        lesson_t = []
        for table in lesson_tables:
            lesson_infos = self.ctrl.get_lessoninfos(table.id)
            infos = []
            for info in lesson_infos:
                #TODO for_class and for_semester
                course = Course(gid=info.course.id, name=info.course.name, tearcher=info.course.tearcher, book=info.course.book)
                infos.append(LessonInfo(gid=info.id, course=course, room=info.classroom, weekday=info.weekday, start=info.start, duration=info.duration))
            lesson_t.append(LessonTable(gid=table.id, user_id=table.user_id, semester=table.semester, lessoninfos=infos))
        return lesson_t

    def create_lessontable(self, auth_token):
        return self.ctrl.create_lessontable(auth_token)

    def dept_provinces(self, auth_token):
        return self.ctrl.dept_provinces();

    def dept_schools(self, auth_token, province):
        return self.ctrl.dept_schools(province)

    def dept_departments(self, auth_token, province, school):
        return self.ctrl.dept_departments(province, school)

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
