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
