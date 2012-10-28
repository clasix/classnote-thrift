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

#reload(sys)
#sys.setdefaultencoding("utf-8")

config = {'dev_mode': False, 'mysql_user': sys.argv[1], 'mysql_passwd': sys.argv[2]}
if len(sys.argv) > 3:
    config['host'] = sys.argv[3]
import model
db = model.db_factory(config)
from ctrl import Ctrl
ctrl = Ctrl(db)

from handler import ClassNoteHandler
handler = ClassNoteHandler(ctrl)
processor = ClassNote.Processor(handler)
transport = TSocket.TServerSocket(host='0.0.0.0', port=8080)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

# TServer.TSimpleServer
# TServer.TThreadedServer
# TServer.TThreadPoolServer
# TServer.TForkingServer
server = TServer.TForkingServer(processor, transport, tfactory, pfactory)

# You could do one of these for a multithreaded server
#server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
#server = TServer.TThreadPoolServer(processor, transport, tfactory, pfactory)

print 'Starting the server...'
server.serve()
print 'done.'
