#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import mapper, sessionmaker

engine = create_engine('sqlite:///:memory:', echo=False)
engine.connect().connection.connection.text_factory = str
metadata = MetaData()

table = Table('projects', metadata, 
        Column('id', Integer, primary_key=True),Column('name', String(50)))

class Project(object):
    def __init__(self, name):
        self.name = name

mapper(Project, table)
metadata.create_all(engine)

session = sessionmaker(bind=engine)()

project = Project("Lorem ipsum你好")

print(type(project.name))

session.add(project)
session.commit()

names = session.query(Project.name).group_by(Project.name).first()[0]

print names

print project.name
print(type(project.name))
