# -*- coding: utf-8 -*-

import sys
from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

sys.path.append('../gen-py')

from helloworld import HelloWorld
from helloworld.ttypes import *     # NOQA
from helloworld.constants import *  # NOQA


try:
    # Make socket
    transport = TSocket.TSocket('localhost', 10088)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = HelloWorld.Client(protocol)

    # Connect!
    transport.open()

    client.ping()

    print client.echo('echo msg from server side')

    transport.close()
except Thrift.TException, tx:
    print "%s" % (tx.message)
