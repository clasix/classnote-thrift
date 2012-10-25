#!/usr/bin/env python

import sys
sys.path.append('../gen-py')

from service import ClassNote
from service.ttypes import *
from type.ttypes import *

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

try:

  # Make socket
  transport = TSocket.TSocket('clasix.tk', 8080)

  # Buffering is critical. Raw sockets are very slow
  transport = TTransport.TBufferedTransport(transport)

  # Wrap in a protocol
  protocol = TBinaryProtocol.TBinaryProtocol(transport)

  # Create a client to use the protocol encoder
  client = ClassNote.Client(protocol)

  # Connect!
  transport.open()

  res = client.sign_up_email('test@gmail.com', '12345')
  print res
  if res:
    auth_token = client.login_by_email('test@gmail.com', '12345')
    print 'auth_token is %s' % auth_token
    res = client.sign_out(auth_token.auth_token)
    print 'Sign out is %s' % res

  # Close!
  transport.close()

except Thrift.TException, tx:
  print '%s' % (tx.message)
