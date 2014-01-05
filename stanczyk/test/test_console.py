from stanczyk import consoleFunctions
from stanczyk.console import LineKillingConsoleManhole, Protocol
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
        self.assertEqual(afterHome, expectedAfterHome)


    def test_consoleFunctions(self):
        """The manhole's namespace contains itself, under the ``"manhole"``
        name, as well as all of the console functions under their own
        names, partially applied with the manhole's namespace.

        """
        expectedKwargs = {"namespace": self.protocol.namespace}
        gotFuncs = set()
        for name, obj in self.protocol.namespace.iteritems():
            if name == "manhole":
                self.assertEqual(obj, self.protocol)
            else:
                self.assertEqual(obj.__name__, name)
                self.assertEqual(obj.keywords, expectedKwargs)
                gotFuncs.add(obj.func)

        self.assertEqual(gotFuncs, set(consoleFunctions))



ERASE_DISPLAY = '\x1b[2J'
CURSOR_HOME = '\x1b[H'

expectedAfterHome = "\r\n".join("""
Welcome to the Crypto 101 console client!


The following commands are available:
+--------------+-----------------------------------------------------+
|     Name     |                     Description                     |
+==============+=====================================================+
| connect      | Connects to the Crypto 101 exercise server.         |
+--------------+-----------------------------------------------------+
| connectProxy | Proxy connections server with the given identifier. |
+--------------+-----------------------------------------------------+

(Crypto101) >>> """.split("\n"))
