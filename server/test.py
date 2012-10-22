#!/usr/bin/env python
# -*- coding: utf-8 -*-

config = {'dev_mode': True, 'sqlite_path': 'init.db'}
import model
db = model.db_factory(config)
from ctrl import Ctrl
ctrl = Ctrl(db)
