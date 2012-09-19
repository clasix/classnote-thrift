#!/usr/bin/env python

import sys
sys.path.append('../gen-py')

from service import ClassNote
from type.ttypes import *
from service.ttypes import *

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

config = {'dev_mode': True, 'sqlite_path': 'thrift.db'}
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

#handler = ClassNoteHandler()
processor = ClassNote.Processor(ctrl)
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
