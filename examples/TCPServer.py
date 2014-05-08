# -*- coding: utf-8 -*-

import sys
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

sys.path.append('../gen-py')

from helloworld import HelloWorld
from helloworld.ttypes import *  # NOQA


class HelloWorldHandler(object):

    def ping(self):
        print "ping ..."

    def echo(msg):
        return msg


handler = HelloWorldHandler()
processor = HelloWorld.Processor(handler)
transport = TSocket.TServerSocket(port=10088)
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()
server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)


if __name__ == '__main__':
    print "Starting python server..."
    server.serve()
    print "done!"
