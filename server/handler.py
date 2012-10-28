#!/usr/bin/env python
# -*- coding: utf-8 -*-

# implate thrift service api
import sys
sys.path.append('../gen-py')
import model
from type.ttypes import *
from exception.ttypes import Exception, ExceptionCode as ecode

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

    def dept_code(self, auth_token, province, school, dept):
        dept_code = self.ctrl.dept_code(province, school, dept)

        if dept_code is None:
            return Exception(ecode.NOT_FOUND)
        return dept_code

    def getSyncState(self, auth_token):
        user_id = self.ctrl.get_user_id(auth_token)
        if user_id is not None:
            user_sync = self.ctrl.user_sync_by_userid(user_id)
            return SyncState(currentTime = datetime.datetime.utcnow, fullSyncBefore = user_sync.fullSyncBefore, updateCount = user_sync.updateCount) 
        return Exception(ecode.PERMISSION_DENIED)

    def getSyncChunk(self, auth_token, afterUSN, maxEntries, fullSyncOnly):
        user_id = self.ctrl.get_user_id(auth_token)
        if user_id is not None:
            user_sync_state = self.ctrl.user_sync_by_userid(user_id)
            updateCount = user_sync_state.updateCount
            currentTime = datetime.datetime.utcnow
            chunkHighUSN = None
            lessonTables = self.ctrl.lesson_table_for_user(user_id)
            tableitems = []
            for lessonTable in lessonTables:
                tableitems.extend(self.ctrl.sync_chunk_lessontableitems(lessonTable.table_id, afterUSN, maxEntries))
            if len(tableitems) > 0:
                chunkHighUSN = tableitems[-1].updateSeqNum
            lesson_table_items = [LessonTableItem(gid=i.id, table_id=i.table_id, lesson_info_id=i.lesson_info_id, updateSequenceNum=i.updateSeqNum) for i in tableitems]
            sync_chunk = SyncChunk(currentTime = currentTime, updateCount=updateCount, lessonTableItems=lesson_table_items)
            if chunkHighUSN is not None:
                sync_chunk.chunkHighUSN = chunkHighUSN
            return sync_chunk
        return Exception(ecode.PERMISSION_DENIED)

    def getFilterSyncChunk(self, auth_token, afterUSN, maxEntries, filter):
        pass

    def getSchoolLessonSyncState(self, auth_token, school_code):
        school_sync = self.ctrl.school_sync_by_schoolcode(school_code)
        return SyncState(currentTime = datetime.datetime.utcnow, fullSyncBefore = school_sync.fullSyncBefore, updateCount = school_sync.updateCount) 

    def getSchoolLessonSyncChunk(self, auth_token, school_code, afterUSN, maxEntries, fullSynOnly):
        user_id = self.ctrl.get_user_id(auth_token)
        if user_id is not None:
            school_sync_state = self.ctrl.school_sync_by_schoolcode(school_code)
            updateCount = school_sync_state.updateCount
            currentTime = datetime.datetime.utcnow
            chunkHighUSN = None
            courses = self.ctrl.sync_chunk_courses(school_code, afterUSN, maxEntries)
            if len(courses) > 0:
                chunkHighUSN = courses[-1].updateSeqNum
            sync_courses = [Course(gid=i.id, name=i.name,tearcher=i.tearcher,book=i.book,school_code=i.school_code, dept_code=i.dept_code, semester=i.semester, year=i.year, updateSequenceNum=i.updateSeqNum) for i in courses]
            sync_chunk = SyncChunk(currentTime = currentTime, updateCount=updateCount, courses=sync_courses)
            if chunkHighUSN is not None:
                sync_chunk.chunkHighUSN = chunkHighUSN
            return sync_chunk
        return Exception(ecode.PERMISSION_DENIED)


    def createCourse(self, auth_token, course):
        user_id = self.ctrl.get_user_id(auth_token)
        if user_id is not None:
            i = self.ctrl.createCourse(course)
            return Course(gid=i.id, name=i.name,tearcher=i.tearcher,book=i.book,school_code=i.school_code, dept_code=i.dept_code, semester=i.semester, year=i.year, updateSequenceNum=i.updateSeqNum)
        return Exception(ecode.PERMISSION_DENIED)


    def updateCourse(self, auth_token, course):
        user_id = self.ctrl.get_user_id(auth_token)
        if user_id is not None:
            return self.ctrl.updateCourse(course)
        return Exception(ecode.PERMISSION_DENIED)
    
    def expungeCourse(self, auth_token, guid):
        user_id = self.ctrl.get_user_id(auth_token)
        if user_id is not None:
            return self.ctrl.expungeCourse(guid)
        return Exception(ecode.PERMISSION_DENIED)

    def user_get(self, auth_token, user_id):
        pass

