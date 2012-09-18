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

from sqlalchemy import create_engine
from sqlalchemy import Table, Column, MetaData, ForeignKey
from sqlalchemy import BigInteger, Boolean, String, Date, DateTime, Float, Integer
from sqlalchemy import PickleType, Unicode, UnicodeText
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper, sessionmaker, relation, synonym
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import asc
from auth import AuthUser

SQLModel = declarative_base()

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
