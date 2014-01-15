from stanczyk.protocol import Factory, Protocol
from stanczyk.test.util import FakeManhole
from twisted.trial.unittest import SynchronousTestCase


class ProtocolTests(SynchronousTestCase):
    def setUp(self):
        self.manhole = FakeManhole()
        self.namespace = {"manhole": self.manhole}
        self.factory = Factory(self.namespace)
        self.protocol = Protocol()
        self.protocol.factory = self.factory


    def test_namespace(self):
        """The protocol has access to the factory's namespace, through its
        own ``namespace`` attribute.

        """
        self.assertIdentical(self.protocol.namespace, self.namespace)


    def test_notifySolved(self):
        """When an exercise is solved, the user is notified on the console.

        """
        result = self.protocol.notifySolved("xyzzy", u"The title")
        self.assertEqual(result, {})
        self.assertEquals(self.manhole.line, "\nCongratulations! You have "
                          "solved the xyzzy excercise (The title).")
