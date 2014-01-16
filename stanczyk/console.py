from collections import OrderedDict
from functools import partial, update_wrapper
from inspect import getargspec
from stanczyk import consoleFunctions
from texttable import Texttable
from twisted.conch.stdio import ConsoleManhole
from twisted.internet.defer import inlineCallbacks

CTRL_K = "\x0b" # vertical tab


class LineKillingConsoleManhole(ConsoleManhole):
    """A console manhole that makes C-k do what you expect (kill until
    end-of-line).

    """
    def connectionMade(self):
        ConsoleManhole.connectionMade(self)
        self.keyHandlers[CTRL_K] = self._killRestOfLine


    def _killRestOfLine(self):
        """Kills the rest of the line, like Emacs' kill-line.

        """
        self.terminal.eraseToLineEnd()
        del self.lineBuffer[self.lineBufferIndex:]



class Protocol(LineKillingConsoleManhole):
    ps = "(Crypto101) >>> ", "(Crypto101) ... "

    def __init__(self):
        LineKillingConsoleManhole.__init__(self)

        self.namespace = namespace = OrderedDict({"manhole": self})
        for f in consoleFunctions:
            partiallyApplied = partial(f, namespace=namespace)
            namespace[f.__name__] = update_wrapper(partiallyApplied, f)


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

        table = Texttable()
        table.header(["Command", "Description"])
        for name, obj in self.namespace.iteritems():
            if obj is self:
                continue
            shortDoc = _extractFirstParagraphOfDocstring(obj)
            command = _formatFunction(obj.func)
            table.add_row([command, shortDoc])

        # Ugh! I'm only giving Texttable bytes; why is it giving me unicode?
        self.terminal.write(table.draw().encode("utf-8"))

        self.terminal.nextLine()
        self.terminal.nextLine()

        self.drawInputLine()


    @inlineCallbacks
    def overwriteLine(self, line):
        """Overwrites the current line of the terminal with the given line,
        and then redraws the input line.

        """
        yield self.killWholeLine()
        self.terminal.write(line)
        self.terminal.nextLine()
        yield self.killWholeLine()
        self.drawInputLine()


    @inlineCallbacks
    def killWholeLine(self):
        """Erases the entire current line and moves the cursor to the
        beginning of it.

        """
        _x, y = yield self.terminal.reportCursorPosition()
        self.terminal.cursorPosition(0, y)
        self.terminal.eraseLine()



MOTD = """
Welcome to the Crypto 101 console client!

"""


def _extractFirstParagraphOfDocstring(f):
    """Extracts the first paragraph of the docstring of the given
    function.

    Also fixes extraneous whitespace due to indentation.
    """
    firstParagraph = f.__doc__.split("\n\n", 1)[0]
    lines = [line.strip() for line in firstParagraph.split("\n")]
    return " ".join(lines)


def _extractArgs(f):
    """Extracts all mandatory args of the function, minus the "namespace"
    argument, as well as all the public optional args of the function.
    Public args are defined as args that don't start with an underscore.

    """
    spec = getargspec(f)

    if spec.defaults is not None: # Chop off all of the optional args
        mandatory = spec.args[:-len(spec.defaults)]
        optionalNames = spec.args[-len(spec.defaults):]
        optional = zip(optionalNames, spec.defaults)
    else: # There are no optional args, so all args are mandatory
        mandatory = spec.args
        optional = []

    mandatory = [a for a in mandatory if a != "namespace"]
    optional = [(n, v) for (n, v) in optional if not n.startswith("_")]
    return mandatory, optional


def _formatFunction(f):
    """Pretty-format the function.

    """
    mandatory, optional = _extractArgs(f)
    argSpecs = mandatory + ["{}={}".format(n, v) for (n, v) in optional]
    return "{}({})".format(f.__name__, ", ".join(argSpecs))
