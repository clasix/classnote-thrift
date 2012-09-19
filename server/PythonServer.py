#!/usr/bin/env python

#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements. See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership. The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied. See the License for the
# specific language governing permissions and limitations
# under the License.
#

import sys
sys.path.append('../gen-py')

from service import ClassNote
from type.ttypes import *
from service.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

config = {'dev_model': True, 'sqlite_path': 'thrift.db'}
import model
db = model.db_factory(config)
from ctrl import Ctrl
ctrl = Ctrl(db)

class ClassNoteHandler:
  def __init__(self):
    self.log = {}

  def login_by_mail(self, client_id, client_secret, mail, password):
    pass

  def logout(self, access_token):
    pass

  def ping(self, input):
    return "ping input: %s" % (input)

  def user_get(self, access_token, gid):
    pass

  def user_set(self, access_token, user):
    pass

handler = ClassNoteHandler()
processor = ClassNote.Processor(handler)
transport = TSocket.TServerSocket(port=9090)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

# You could do one of these for a multithreaded server
#server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
#server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'
