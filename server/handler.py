#!/usr/bin/env python
# -*- coding: utf-8 -*-

# implate thrift service api
class ClassNoteHandler:
    def __init__(self, ctrl):
        self.log = {}
        self.ctrl = ctrl

    def login_by_mail(self, email, password):
        return self.ctrl.login_by_email(email, password)

    def login_by_username(self, username, password)
        return self.ctrl.login_by_username(username, password)

    def sign_up_email(self, email, password):
        return self.ctrl.sign_up_email(email, password)

    def sign_up_username(self, username, password):
        return self.ctrl.sign_up_username(username, password)

    def sign_out(self, auth_token)
        return self.ctrl.sign_out(auth_token)
