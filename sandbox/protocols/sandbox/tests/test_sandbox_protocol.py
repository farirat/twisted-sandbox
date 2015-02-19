"""
Test cases for Sandbox TCP client
"""

from twisted.internet import reactor, defer
from twisted.trial.unittest import TestCase
from twisted.internet.protocol import Factory 
from sandbox.protocols.sandbox.tests import simulators
from sandbox.protocols.sandbox import sandbox

class SimulatorTestCase(TestCase):
    protocol = simulators.SandboxProtocol
       
    def setUp(self):
        self.sbServerFactory = Factory()
        self.sbServerFactory.protocol = self.protocol
        self.sbServer = reactor.listenTCP(0, self.sbServerFactory)
        
    def tearDown(self):
        self.sbServer.stopListening()

class StatusTestCase(SimulatorTestCase):
    @defer.inlineCallbacks
    def setUp(self):
        SimulatorTestCase.setUp(self)

        self.sbClientFactory = sandbox.SandboxFactory()
        self.sbClient = yield self.sbClientFactory.connect('127.0.0.1', self.sbServer.getHost().port)

    @defer.inlineCallbacks
    def tearDown(self):
        SimulatorTestCase.tearDown(self)

        yield self.sbClient.transport.loseConnection()

    @defer.inlineCallbacks
    def test_get_status(self):
        c = yield self.sbClient.sendRequest('Do you hear me ?')
        print c