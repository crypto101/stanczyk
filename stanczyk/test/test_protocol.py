from stanczyk.protocol import connect, Factory, Protocol
from stanczyk.test.util import CommandTestMixin, FakeManhole, FakeRemote
from twisted.test.proto_helpers import MemoryReactor
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



class ConnectTests(CommandTestMixin, SynchronousTestCase):
    def test_connect(self):
        reactor = MemoryReactor()

        self.assertNotIn("remote", self.namespace)

        result = connect(namespace=self.namespace, _reactor=reactor)
        self.assertIdentical(result, None)

        host, port, factory, _ctxFactory, _, _ = reactor.sslClients[0]
        self.assertEqual(host, "localhost")
        self.assertEqual(port, 4430)

        factory._onConnection.callback(None)
        self.assertIn("remote", self.namespace)

        line = self.manhole.line
        self.assertEqual(line, "Connected to the exercise server!")


    def test_alreadyConnected(self):
        """If the client is already connected, an exception is raised.

        """
        namespace = {"remote": FakeRemote()}
        self.assertRaises(RuntimeError, connect, namespace=namespace)
