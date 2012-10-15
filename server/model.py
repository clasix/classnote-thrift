#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""We use SQLAlchemy_ in declarative_ mode.
  
    .. _SQLAlchemy: http://www.sqlalchemy.org/
    .. _declarative: http://www.sqlalchemy.org/docs/reference/ext/declarative.html
"""

import logging
import os
import sys
import datetime
import uuid

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, MetaData, ForeignKey
from sqlalchemy import BigInteger, Boolean, String, Date, DateTime, Float, Integer
from sqlalchemy import PickleType, Unicode, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, relation, synonym, relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import asc
from auth import AuthUser

SQLModel = declarative_base()

AUTH_TOKEN_LENGTH = 20

class User(SQLModel, AuthUser):
    """
    """

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)

    username = Column(String(80))
    password = Column(String(120))
    salt = Column(String(80))
    email = Column(String(80), unique=True)
    activate = Column(Boolean, default=False)
    created = Column(DateTime(), default=datetime.datetime.utcnow)

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        password = kwargs.get('password')
        if password is not None:
            self.created = datetime.datetime.utcnow()
            self.set_and_encrypt_password(password)

    def __getstate__(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created': self.created
        }

    def __repr__(self):
        return '<User id="%s">' % self.id

class Class(SQLModel):
    """
    """

    __tablename__ = 'classes'
    id = Column(Integer, primary_key=True, nullable=False)

    school = Column(String(80))
    dept = Column(String(80))
    year = Column(Integer)

class Course(SQLModel):
    """
    """

    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True, nullable=False)

    name = Column(String(80))
    tearcher = Column(String(80))
    book = Column(String(80))
    for_class = Column(Integer) # if -1, means every class can choose
    for_semester = Column(Integer) # if -1, meas every semester can choose

class LessonInfo(SQLModel):
    """
    """

    __tablename__ = 'lessoninfos'
    id = Column(Integer, primary_key=True, nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'))
    classroom = Column(String(80))
    weekday = Column(Integer)
    start = Column(Integer)
    duration = Column(Integer)
    course = relationship(Course, primaryjoin=course_id == Course.id)

class LessonTable(SQLModel):
    """
    """
    __tablename__ = 'lessontables'
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id')) # class_id, the sharedTable for a class
    semester = Column(Integer)
    user = relationship(User, primaryjoin=user_id == User.id)

class LessonTableItem(SQLModel):
    """
    """
    __tablename__ = 'lessontableitems'
    id = Column(Integer, primary_key=True, nullable=False)

    table_id = Column(Integer, ForeignKey('lessontables.id'))
    lesson_info_id = Column(Integer, ForeignKey('lessoninfos.id'))
    table = relationship(LessonTable, primaryjoin=table_id == LessonTable.id)
    lesson_info = relationship(LessonInfo, primaryjoin=lesson_info_id == LessonInfo.id)


class AuthToken(SQLModel):
    """
    """

    __tablename__ = 'authtokens'
    id = Column(Integer, primary_key=True, nullable=False)

    user_id = Column(Integer, ForeignKey('users.id'))
    auth_token = Column(String(20), unique=True)
    user = relationship(User, primaryjoin=user_id == User.id)

    def __init__(self, *args, **kwargs):
        super(AuthToken, self).__init__(*args, **kwargs)

    def __getstate__(self):
        return self.__dict__

    def __repr__(self):
        return '<AuthToken auth_token="%s">' % self.auth_token

    @classmethod
    def uuid_token(cls, db):
        auth_token = uuid.uuid4().hex[:AUTH_TOKEN_LENGTH]
        while (db.query(AuthToken).filter(AuthToken.auth_token==auth_token).first()):
            auth_token = uuid.uuid4().hex[:AUTH_TOKEN_LENGTH]
        return auth_token

def db_factory(settings):
    """
    """

    import logging
    logging.info(settings)

    # use sqlite in dev
    if settings['dev_mode']:
        sqlite_path = 'sqlite:///%s' % os.path.abspath(settings['sqlite_path'])
        engine = create_engine(sqlite_path, echo=True)
    else: # use postgresql in production
        raise NotImplementedError
    SQLModel.metadata.create_all(engine)
    Session = sessionmaker(bind=engine, autocommit=True)
    session = Session()
    return session

def bootstrap(session):
    """ Populate the database
    """

    session.begin()

    # commit changes
    try:
        session.commit()
    except IntegrityError, err:
        logging.error(err)
        session.rollback()
