from stanczyk.console import LineKillingConsoleManhole, MOTD, Protocol, namespace
from twisted.conch.insults.insults import ServerProtocol
from twisted.test.proto_helpers import StringTransport
from twisted.trial.unittest import SynchronousTestCase


class TerminalSetUp(object):
    """Set-up for in-memory terminal testing.

    """
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



class ProtocolLineKillingTests(LineKillingTests):
    """Tests for the protocol.

    By inheriting from ``LineKillingTests``, we assert that line
    killing also works for the protocol.

    """
    protocolClass = Protocol

    def test_sessionStarted(self):
        """On start-up, the terminal is cleared, cursor put in the home
        position, MOTD printed, and the input line drawn.

        """
        allBytes = self.transport.value()
        _beforeClear, afterClear = allBytes.split(ERASE_DISPLAY, 1)
        beforeHome, afterHome = afterClear.split(CURSOR_HOME, 1)
        self.assertEqual(beforeHome, "")
        motdWithPrompt = "\r\n".join(MOTD.split("\n")) + Protocol.ps[0]
        self.assertEqual(afterHome, motdWithPrompt)


    def test_namespace(self):
        """The manhole is created with the console's namespace.

        """
        self.assertEqual(self.protocol.namespace, namespace)



ERASE_DISPLAY = '\x1b[2J'
CURSOR_HOME = '\x1b[H'
