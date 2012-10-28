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
        provinces = [i[0].encode("UTF-8") for i in provinces]
        return provinces

    def dept_schools(self, province):
        try:
            schools = self.db.query(Dept.school).filter(Dept.province == province).group_by(Dept.school).all()
        except NoResultFound:
            schools = []
        schools = [i[0].encode("UTF-8") for i in schools]
        return schools

    def dept_departments(self, province, school):
        try:
            departments = self.db.query(Dept.dept).filter(Dept.province==province, Dept.school==school).group_by(Dept.dept).all()
        except NoResultFound:
            departments = []
        departments = [i[0].encode("UTF-8") for i in departments]
        return departments

    def dept_code(self, province, school, dept):
        try:
            dept_code = self.db.query(Dept.code).filter(Dept.province==province, Dept.school==school, Dept.dept=dept).one()
        except NoResultFound:
            dept_code = None
        return dept_code

    def user_sync_by_userid(self, user_id):
        try:
            user_sync = self.db.query(UserSyncStore).filter(UserSyncStore.user_id==user_id).first()
        except NoResultFound:
            user_sync = UserSyncStore(user_id, 0)
            self.db.add(user_sync)
        return user_sync

    def school_sync_by_schoolcode(self, school_code):
        try:
            school_sync = self.db.query(SchoolSyncStore).filter(SchoolSyncStore.school_code==school_code).first()
        except NoResultFound:
            school_sync = SchoolSyncStore(school_code, 0)
            self.db.add(school_sync)
        return school_sync

    def plus_updateCount_school(self, school_code):
        self.db.begin()
        state = self.school_sync_by_schoolcode(school_code)
        state.updateCount = state.updateCount + 1
        self.db.commit()
        return state.updateCount

    def plus_updateCount_user(self, user_id):
        self.db.begin()
        state = self.user_sync_by_userid(user_id)
        state.updateCount = state.updateCount + 1
        self.db.commit()
        return state.updateCount

    def sync_chunk_lessontableitems(self, table_id, afterUSN, maxEntries):
        try:
            sync_lessontableitems = self.db.query(LessonTableItem).filter(LessonTableItem.table_id==table_id, LessonTableItem.updateSeqNum>afterUSN).order_by(LessonTableItem.updateSeqNum.asc()).limit(maxEntries)
        except NoResultFound:
            sync_lessontableitems = []
        return sync_lessontableitems

    def sync_chunk_courses(self, school_code, afterUSN, maxEntries):
        try:
            sync_courses = self.db.query(Course).filter(Course.school_code==school_code, Course.updateSeqNum>afterUSN).order_by(Course.updateSeqNum.asc()).limit(maxEntries)
        except NoResultFound:
            sync_courses = []
        return sync_courses

    def lesson_table_for_user(self, user_id):
        try:
            lessonTables = self.db.query(LessonTable).filter(LessonTable.user_id==user_id).all()
        except NoResultFound:
            lessonTables = []
        return lessonTables

    def createCourse(self, course):
        course = Course(name=course.name, tearcher=course.tearcher, book=course.book, school_code=course.school_code, dept_code=course.dept_code, semester=course.semester, year=course.year, updateSeqNum=self.plus_updateCount_school(course.school_code))
        self.db.add(course)
        self.db.commit()
        return course

    def updateCourse(self, course):
        self.db.begin()
        course = self.db.query(Course).filter(Course.id == course.gid).first()
        course.updateSeqNum = self.plus_updateCount_school(course.school_code)
        self.db.commit()
        return course.updateSeqNum

    def expungeCourse(self, guid):
        self.db.begin()
        course = self.db.query(Course).filter(Course.id == guid).first()
        updateSeqNum = self.plus_updateCount_school(course.school_code)
        self.db.delete(course)
        self.db.commit()
        return updateSeqNum
