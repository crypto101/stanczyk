from stanczyk.proxy import connectProxy
from stanczyk.test.util import ConnectedCommandTestMixin
from twisted.trial.unittest import SynchronousTestCase
from twisted.test.proto_helpers import MemoryReactor


class ConnectProxyTests(ConnectedCommandTestMixin, SynchronousTestCase):
    command = staticmethod(connectProxy)
    kwargs = {"identifier": "xyzzy"}

    def test_connect(self):
        """When a user initiates a proxy connection, it starts listening on a
        randomly available local port with a proxying factory with the
        requested identifier. Once it has started listening, it
        notifies the user. The command returns None.

        """
        reactor = MemoryReactor()

        result = connectProxy("xyzzy", self.namespace, _reactor=reactor)
        self.assertIdentical(result, None)

        port, factory, _backlog, interface = reactor.tcpServers[0]
        self.assertEqual(port, 0)
        self.assertEqual(interface, "localhost")
        self.assertEqual(self.manhole.line, 'xyzzy is now listening on 0.0.0.0:0')
