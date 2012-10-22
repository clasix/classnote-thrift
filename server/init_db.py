#!/usr/bin/env python
# -*- coding: utf-8 -*-
from model import Dept

config = {'dev_mode':True, 'sqlite_path': 'init.db'}
import model

db = model.db_factory(config)

import re
import codecs
import sys
reload(sys)

sys.setdefaultencoding('utf8')

class Init:
    def init_Dept(self, db):
        f = codecs.open('../exclude/DepartmentList.txt', 'r', 'utf8')
        area = re.compile(r"\[\".+\"\]")
        dept = re.compile(r"\".+\"")
        lines = f.readlines()
        area_str = ""
        univ_str = ""
        dept_str = ""
        for line in lines:
            if line[-2:] == '\r\n':
                line = line[0: -2]
            if line[-1:] == '\n':
                line = line[0: -1]
            if line[-2:] == '"]':
                area_str = area.search(line).group()[2:-2].split('_')[1]
            elif line[-2:] == '")':
                univ_str = area.search(line).group()[2:-2]
            elif line[-1:] == '"':
                dept_str = dept.search(line).group()[1:-1]
                dept_obj = Dept(province=area_str, school=univ_str, dept=dept_str) 
                db.add(dept_obj)
        f.close()

db.begin()
init = Init()
init.init_Dept(db)

db.commit() 
