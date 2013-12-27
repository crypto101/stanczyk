from clarent import certificate, path
from twisted.internet import endpoints, protocol, reactor
from twisted.protocols import amp
from txampext import multiplexing


class Protocol(multiplexing.ProxyingAMPLocator, amp.AMP):
    """
    Stanczyk's client AMP protocol.
    """



class Factory(protocol.ReconnectingClientFactory):
    """A factory that will reconnect (with exponential backoff).

    """
    protocol = Protocol



def connect(namespace, reactor=reactor):
    """Connects to the Crypto 101 exercise server.

    """
    endpoint = _makeEndpoint(reactor)
    d = endpoint.connect(Factory())
    d.addCallback(_storeRemote, namespace=namespace)
    return d


def _storeRemote(remote, namespace):
    """Stores the remote in the namespace; returns success.

    """
    namespace["remote"] = remote



def _makeEndpoint(reactor):
    ctxFactory = certificate.getContextFactory(path.getDataPath())
    return endpoints.SSL4ClientEndpoint(reactor, "localhost", 4430, ctxFactory)
