from stanczyk import consoleFunctions
from stanczyk.console import LineKillingConsoleManhole, Protocol, _extractArgs
from twisted.conch.insults.helper import TerminalBuffer
from twisted.trial.unittest import SynchronousTestCase


class TerminalSetUp(object):
    """Set-up for in-memory terminal testing.


    """
    protocolClass = None

    def setUp(self):
        self.transport = TerminalBuffer()
        self.protocol = self.protocolClass()
        self.protocol.makeConnection(self.transport)


class LineKillingTests(TerminalSetUp, SynchronousTestCase):
    """Tests for the colored manhole with line killing support.

    """
    protocolClass = LineKillingConsoleManhole

    def test_killLine(self):
        """Receiving a vertical tab (C-k, "\v") kills the rest of the line on
        the terminal, as well as trimming the line buffer.

        """
        for x in list("abcdef") + [self.transport.LEFT_ARROW] * 3:
            self.protocol.keystrokeReceived(x, None)

        self.assertEqual(self.protocol.currentLineBuffer(), ("abc", "def"))

        self.protocol.keystrokeReceived("\v", None)

        self.assertEqual(self.protocol.currentLineBuffer(), ("abc", ""))

        restOfLine = self.transport.lines[self.transport.y][self.transport.x:]
        self.assertTrue(isEmpty(restOfLine))



def notVoids(line):
    """Returns all non-void pairs in a TerminalBuffer line.

    """
    return ((c, a) for (c, a) in line if c is not TerminalBuffer.void)



def chars(line):
    """Returns the chars in a TerminalBuffer line.

    """
    return "".join(c for (c, _) in notVoids(line))



def isEmpty(line):
    """Checks if part of a TerminalBuffer line is empty.

    """
    return not chars(line)



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
        self.assertEqual(str(self.transport), expectedSession)


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


    def test_killWholeLine(self):
        """The killWholeLine method finds the current cursor position, moves
        to the start of that line, and then erases the rest of the
        line.

        """
        for char in "abcdef":
            self.protocol.keystrokeReceived(char, None)

        self.assertTrue(self.getLine())

        oldCoords = self.transport.x, self.transport.y
        self.protocol.killWholeLine()
        self.assertEqual(self.transport.x, 0)
        self.assertEqual(self.transport.y, oldCoords[1])
        self.assertFalse(self.getLine())


    def getLine(self, idx=None):
        """Gets the line with given from the terminal transport. If
        unspecified, gets the current line.

        """
        if idx is None:
            idx = self.transport.y

        return chars(self.transport.lines[idx])


    def test_overwriteLine(self):
        """The overwriteLine method clears the current line, writes the given
        line, moves the cursor to the next line, kills it, and writes an input
        line there.

        """
        for char in "abcdef":
            self.protocol.keystrokeReceived(char, None)

        self.protocol.overwriteLine("the new line")

        self.assertEqual(self.getLine(self.transport.y - 1), "the new line")
        self.assertEqual(self.getLine(), self.protocol.ps[0] + "abcdef")



expectedSession = """
Welcome to the Crypto 101 console client!


The following commands are available:
+--------------------------------------+--------------------------------------+
|               Command                |             Description              |
+======================================+======================================+
| makeCredentials(email)               | Creates credentials to connect to    |
|                                      | the exercise server.                 |
+--------------------------------------+--------------------------------------+
| connect()                            | Connect to the exercise server.      |
+--------------------------------------+--------------------------------------+
| getExercises(solved=False)           | Gets some exercises that are         |
|                                      | currently avaialble to you.          |
+--------------------------------------+--------------------------------------+
| getExerciseDetails(identifier)       | Shows the detailed description of a  |
|                                      | particular excerise.                 |
+--------------------------------------+--------------------------------------+
| connectProxy(identifier)             | Creates a virtual connection to a    |
|                                      | server.                              |
+--------------------------------------+--------------------------------------+

(Crypto101) >>> """



class ExtractArgsTests(SynchronousTestCase):
    def test_noArgs(self):
        """Extracting the args from a function with only an implicit namespace
        argument results in an empty list of mandatory arguments and
        an empty list of optional arguments.

        """
        def f(namespace): pass  # pragma: no cover
        mandatory, optional = _extractArgs(f)
        self.assertEqual(mandatory, [])
        self.assertEqual(optional, [])


    def test_noMandatoryArgs(self):
        """Extracting the args from a function with an implicit namespace
        argument as well as some optional arguments (but no mandatory
        arguments) works correctly.

        """
        def f(namespace, a=1, b=2, c=3): pass  # pragma: no cover

        mandatory, optional = _extractArgs(f)
        self.assertEqual(mandatory, [])
        self.assertEqual(optional, [("a", 1), ("b", 2), ("c", 3)])


    def test_someMandatoryArgs(self):
        """Extracting the args from a function with an implicit namespace
        argument as well as some mandatory arguments works correctly.

        """
        def f(namespace, a, b, c): pass  # pragma: no cover
        mandatory, optional = _extractArgs(f)
        self.assertEqual(mandatory, ["a", "b", "c"])
        self.assertEqual(optional, [])


    def test_bothMandatoryAndOptionalArgs(self):
        """Extracting the args from a function with an implicit namespace
        argument as well as both mandatory and optional arguments
        works correctly.

        Optional arguments that start with an underscore are ignored.
        """
        def f(namespace, a, b, c, d=1, _e=2): pass  # pragma: no cover
        mandatory, optional = _extractArgs(f)
        self.assertEqual(mandatory, ["a", "b", "c"])
        self.assertEqual(optional, [("d", 1)])
