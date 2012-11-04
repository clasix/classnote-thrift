#!/usr/bin/env python
# -*- coding: utf-8 -*-

#config = {'dev_mode': True, 'sqlite_path': 'init.db'}
config = {'dev_mode': False, 'mysql_user': 'clasix', 'mysql_passwd':'clasix', 'host': 'clasix.tk'}
import model
db = model.db_factory(config)
from ctrl import Ctrl
ctrl = Ctrl(db)
