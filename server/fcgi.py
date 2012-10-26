#!/usr/bin/env python
# encoding: utf-8

from app2 import app
from flup.server.fcgi import WSGIServer

WSGIServer(app, bindAddress='/tmp/flask_clasik_tk_app.sock').run()
