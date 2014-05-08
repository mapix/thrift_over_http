# -*- coding: utf-8 -*-

import sys
import base64
from thrift import Thrift
from thrift.transport import THttpClient
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

sys.path.append('../gen-py')

from helloworld import HelloWorld
from helloworld.ttypes import *     # NOQA
from helloworld.constants import *  # NOQA


try:
    username = 'admin'
    password = 'secret'

    # Make socket
    transport = THttpClient.THttpClient('http://localhost:10089/_thrift')
    transport.setCustomHeaders({'Authorization': 'Basic %s' % base64.standard_b64encode(
        '%s:%s' % (username, password)
    )})

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = HelloWorld.Client(protocol)

    # Connect!
    transport.open()

    client.ping()
    print "ping()"

    print client.echo("echo from server side")

    transport.close()
except Thrift.TException, tx:
    print "%s" % (tx.message)
