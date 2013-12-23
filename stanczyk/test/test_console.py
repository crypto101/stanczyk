from stanczyk.console import LineKillingConsoleManhole
from twisted.conch.insults.insults import ServerProtocol
from twisted.test.proto_helpers import StringTransport
from twisted.trial.unittest import SynchronousTestCase


class TerminalSetUp(object):
    protocolClass = None

    def setUp(self):
        self.transport = StringTransport()
        self.terminalTransport = ServerProtocol()
        self.protocol = self.protocolClass()
        self.terminalTransport.protocolFactory = lambda: self.protocol
        self.factory = self.terminalTransport.factory = object()
        self.terminalTransport.makeConnection(self.transport)



class LineKillingTests(TerminalSetUp, SynchronousTestCase):
    protocolClass = LineKillingConsoleManhole

    def test_killLine(self):
        """Receiving a vertical tab (C-k, "\v") kills the rest of the line on
        the terminal, as well as trimming the line buffer.

        """
        self.protocol.lineBuffer = list("abcdef")
        self.protocol.lineBufferIndex = 3
        self.assertEqual(self.protocol.currentLineBuffer(), ("abc", "def"))

        self.transport.clear()
        self.protocol.keystrokeReceived("\v", None)

        self.assertEqual(self.protocol.currentLineBuffer(), ("abc", ""))
        self.assertEqual(self.transport.value(), "\x1b[K")
