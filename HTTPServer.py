# -*- coding: utf-8 -*-

import sys
from flask import Flask, request, make_response
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TTransport

sys.path.append('./gen-py')

from helloworld import HelloWorld
from helloworld.ttypes import *      # NOQA
from helloworld.constants import *   # NOQA


class HelloWorldHandler(object):

    def ping(self):
        print "ping ..."

    def echo(self, msg):
        return msg


handler = HelloWorldHandler()
processor = HelloWorld.Processor(handler)
pfactory = TBinaryProtocol.TBinaryProtocolFactory()
hello_server = TServer.TServer(processor, None, None, None, pfactory, pfactory)

app = Flask(__name__)


@app.route('/_thrift', methods=['POST'])
def _thrift():
    itrans = TTransport.TMemoryBuffer(request.data)
    otrans = TTransport.TMemoryBuffer()
    iprot = hello_server.inputProtocolFactory.getProtocol(itrans)
    oprot = hello_server.outputProtocolFactory.getProtocol(otrans)
    hello_server.processor.process(iprot, oprot)
    return make_response(otrans.getvalue())


if __name__ == '__main__':
    app.run(port=10089)
