"""Test utilities.

"""
from twisted.internet.defer import Deferred
from txampext.multiplexing import ProxyingAMPLocator


class CommandTestMixin(object):
    def setUp(self):
        self.manhole = FakeManhole()
        self.namespace = {"manhole": self.manhole}



class ConnectedCommandTestMixin(CommandTestMixin):
    command, kwargs = None, {}

    def setUp(self):
        CommandTestMixin.setUp(self)
        self.remote = FakeRemote()
        self.namespace["remote"] = self.remote


    def test_mustBeConnected(self):
        """Running the command before being connected raises RuntimeError.

        """
        self.assertRaises(RuntimeError,
                          self.command, namespace={}, **self.kwargs)



class FakeRemote(ProxyingAMPLocator):
    """A fake connected AMP remote.

    Supports the proxying AMP locator API.
    """
    def __init__(self):
        ProxyingAMPLocator.__init__(self)
        self.command = self.kwargs = self.deferred = None


    def callRemote(self, command, **kwargs):
        self.command = command
        self.kwargs = kwargs
        self.deferred = Deferred()
        return self.deferred



class FakeManhole(object):
    def __init__(self):
        self.line = None


    def overwriteLine(self, line):
        self.line = line
