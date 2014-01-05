from collections import OrderedDict
from functools import partial
from stanczyk import consoleFunctions
from twisted.conch.stdio import ConsoleManhole

CTRL_K = "\x0b" # vertical tab


class LineKillingConsoleManhole(ConsoleManhole):
    """A console manhole that makes C-k do what you expect (kill until
    end-of-line).

    """
    def connectionMade(self):
        ConsoleManhole.connectionMade(self)
        self.keyHandlers[CTRL_K] = self._killLine


    def _killLine(self):
        self.terminal.eraseToLineEnd()
        del self.lineBuffer[self.lineBufferIndex:]



class Protocol(LineKillingConsoleManhole):
    ps = "(Crypto101) >>> ", "(Crypto101) ... "

    def __init__(self):
        LineKillingConsoleManhole.__init__(self)

        self.namespace = namespace = OrderedDict({"manhole": self})
        for f in consoleFunctions:
            namespace[f.__name__] = partial(f, namespace=namespace)


    def connectionMade(self):
        """Does ``LineKillingConsoleManhole``'s connection made routine, then
        starts a session.

        """
        LineKillingConsoleManhole.connectionMade(self)
        self._startSession()


    def _startSession(self):
        """Clears terminal, writes a MOTD, and draws the input line.

        """
        self.terminal.eraseDisplay()
        self.terminal.cursorHome()
        self.terminal.write(MOTD)

        self.terminal.write("\nThe following commands are available:\n")
        for name, obj in self.namespace.iteritems():
            if obj is self:
                continue
            firstLine = obj.func.__doc__.split("\n", 1)[0]
            self.terminal.write("{}: {}\n".format(name, firstLine))
        self.terminal.write("\n")

        self.drawInputLine()


    def writeLine(self, line):
        """
        Writes a line to the terminal, and then redraws the input line.
        """
        self.terminal.eraseToLineBeginning()
        self.terminal.write(line)
        self.terminal.nextLine()
        self.drawInputLine()



MOTD = """
Welcome to the Crypto 101 console client!

"""
