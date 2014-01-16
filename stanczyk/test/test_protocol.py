from clarent import certificate
from errno import ENOENT
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
        """Attempts to connect. The client already has credentials in the
        appropriate place, and the client is not connected already.
        Asserts that stanczyk attempts to connect to the appropriate
        place.

        """
        reactor = MemoryReactor()
        fakeCtxFactory = object()
        self.patch(certificate, "getContextFactory", lambda _path: fakeCtxFactory)

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


    def test_unregistered(self):
        """When the user has not yet created any credentials, a useful error
        message is displayed.

        """
        def raiser(_path):
            raise IOError(ENOENT, "No such file or directory: '/yeah/ok/w/e'")
        self.patch(certificate, "getContextFactory", raiser)

        result = connect(namespace=self.namespace)
        self.assertIdentical(result, None)

        self.assertEqual(self.manhole.line, "Couldn't find your credentials. "
                         "Did you call 'makeCredentials'?")
