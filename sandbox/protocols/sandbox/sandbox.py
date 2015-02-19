import logging
from collections import deque
from twisted.internet import reactor, defer
from twisted.internet.protocol import Protocol
from twisted.internet.protocol import ClientFactory

LOG_CATEGORY="fourat.protocols.sandbox"

class SandboxProtocol(Protocol):
    def __init__(self):
        self.log = logging.getLogger(LOG_CATEGORY)

    def connectionMade(self):
        Protocol.connectionMade(self)

        self.deferreds = deque()
        self.factory.connectedDeferred.callback(self)

        self.log.info('Connected to %s:%s.' % (self.transport.getPeer().host,
            self.transport.getPeer().port))

    def connectionLost(self, reason):
        for d in list(self.deferreds):
            d.errback(reason)
        self.deferreds.clear()

    def dataReceived(self, data):
        self.log.debug('dataReceived: %s' % data)

        d = self.deferreds.popleft()
        d.callback(data)

    def sendRequest(self, data):
        self.transport.write( data )

        d = defer.Deferred()
        self.deferreds.append(d)
        return d

class SandboxFactory(ClientFactory):
    protocol = SandboxProtocol

    def __init__(self):
        self.log = logging.getLogger(LOG_CATEGORY)

    def connect(self, host, port):
        self.log.info('Establishing TCP connection to %s:%d' % (host, port))
        reactor.connectTCP(host, port, self)

        self.connectedDeferred = defer.Deferred()
        return self.connectedDeferred

    def startedConnecting(self, connector):
        ClientFactory.startedConnecting(self, connector)

        self.log.info('Connecting ..')

    def buildProtocol(self, addr):
        proto = ClientFactory.buildProtocol(self, addr)

        return proto

    def clientConnectionLost(self, connector, reason):
        ClientFactory.clientConnectionLost(self, connector, reason)

        self.log.error('Lost connection.  Reason:', reason)

    def clientConnectionFailed(self, connector, reason):
        ClientFactory.clientConnectionFailed(self, connector, reason)
        
        self.log.error('Lost failed.  Reason:', reason)

        self.connectDeferred.errback(reason)
        self.exitDeferred.callback(None)