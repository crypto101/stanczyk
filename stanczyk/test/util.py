"""Test utilities.

"""
from twisted.internet.defer import Deferred
from twisted.trial.unittest import SynchronousTestCase


class CommandTests(SynchronousTestCase):
    def setUp(self):
        self.remote = FakeRemote()
        self.manhole = FakeManhole()
        self.namespace = {"remote": self.remote, "manhole": self.manhole}



class FakeRemote(object):
    def __init__(self):
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
