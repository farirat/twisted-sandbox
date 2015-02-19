import logging
from twisted.internet import protocol

LOG_CATEGORY="fourat.simulators"

class BlackHoleProtocol( protocol.Protocol ):
    responseMap = {}

    def __init__( self ):
        self.log = logging.getLogger(LOG_CATEGORY)
        self.recvBuffer = ""

    def dataReceived( self, data ):
        self.recvBuffer = self.recvBuffer + data
        self.transport.write( 'This is a blackhole server !' )

class SandboxProtocol(BlackHoleProtocol):
	pass