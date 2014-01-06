from stanczyk import consoleFunctions
from stanczyk.console import LineKillingConsoleManhole, Protocol, _extractArgs
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
+--------------------------------------+--------------------------------------+
|               Command                |             Description              |
+======================================+======================================+
| connect()                            | Connects to the Crypto 101 exercise  |
|                                      | server.                              |
+--------------------------------------+--------------------------------------+
| connectProxy(identifier)             | Start listening on some free local   |
|                                      | port; connections will be proxied to |
|                                      | the virtual server with the given    |
|                                      | identifier.                          |
+--------------------------------------+--------------------------------------+

(Crypto101) >>> """.split("\n"))



class ExtractArgsTests(SynchronousTestCase):
    def test_noArgs(self):
        """Extracting the args from a function with only an implicit namespace
        argument results in an empty list of mandatory arguments and
        an empty list of optional arguments.

        """
        def f(namespace): pass
        mandatory, optional = _extractArgs(f)
        self.assertEqual(mandatory, [])
        self.assertEqual(optional, [])


    def test_noMandatoryArgs(self):
        """Extracting the args from a function with an implicit namespace
        argument as well as some optional arguments (but no mandatory
        arguments) works correctly.

        """
        def f(namespace, a=1, b=2, c=3): pass

        mandatory, optional = _extractArgs(f)
        self.assertEqual(mandatory, [])
        self.assertEqual(optional, [("a", 1), ("b", 2), ("c", 3)])


    def test_someMandatoryArgs(self):
        """Extracting the args from a function with an implicit namespace
        argument as well as some mandatory arguments works correctly.

        """
        def f(namespace, a, b, c): pass
        mandatory, optional = _extractArgs(f)
        self.assertEqual(mandatory, ["a", "b", "c"])
        self.assertEqual(optional, [])


    def test_bothMandatoryAndOptionalArgs(self):
        """Extracting the args from a function with an implicit namespace
        argument as well as both mandatory and optional arguments
        works correctly.

        Optional arguments that start with an underscore are ignored.
        """
        def f(namespace, a, b, c, d=1, _e=2): pass
        mandatory, optional = _extractArgs(f)
        self.assertEqual(mandatory, ["a", "b", "c"])
        self.assertEqual(optional, [("d", 1)])
