# -*- coding: utf-8 -*-

import sys
from functools import wraps
from flask import Flask, g, request, make_response
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer
from thrift.transport import TTransport

sys.path.append('../gen-py')

from helloworld import HelloWorld
from helloworld.ttypes import *      # NOQA
from helloworld.constants import *   # NOQA


def check_auth(username, password):
    return username == 'admin' and password == 'secret'


def requires_authorization(failure):
    def _requires_authorization(func):
        @wraps(func)
        def _(*args, **kwargs):
            auth = request.authorization
            if not auth or not check_auth(auth.username, auth.password):
                return failure
            g.user = auth.username
            return func(*args, **kwargs)
        return _
    return _requires_authorization


class HelloWorldHandler(object):

    def ping(self):
        print "ping ..."

    @requires_authorization('Basic Authenticate required')
    def echo(self, msg):
        return 'Hello %s: %s' % (g.user, msg)


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
