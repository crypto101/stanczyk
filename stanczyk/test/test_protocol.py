from stanczyk.protocol import Factory, Protocol
from twisted.trial.unittest import SynchronousTestCase


class ProtocolTests(SynchronousTestCase):
    def setUp(self):
        self.namespace = {}
        self.factory = Factory(self.namespace)
        self.protocol = Protocol()
        self.protocol.factory = self.factory


    def test_namespace(self):
        """The protocol has access to the factory's namespace, through its
        own ``namespace`` attribute.

        """
        self.assertIdentical(self.protocol.namespace, self.namespace)
