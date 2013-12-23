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
        LineKillingConsoleManhole.__init__(self, namespace)


    def connectionMade(self):
        LineKillingConsoleManhole.connectionMade(self)
        self._startSession()


    def _startSession(self):
        """Clears terminal, writes a MOTD, and draws the input line.

        """
        self.terminal.eraseDisplay()
        self.terminal.cursorHome()
        self.terminal.write(MOTD)
        self.drawInputLine()



namespace = {}



MOTD = """
Welcome to the Crypto 101 console client!
"""
