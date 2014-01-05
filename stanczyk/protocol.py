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

    return None # don't return the deferred, or the REPL will display it


def _storeRemote(remote, namespace):
    """Stores the remote in the namespace; reports success to console.

    """
    namespace["remote"] = remote
    namespace["manhole"].writeLine("Connected to the exercise server!")


def _makeEndpoint(reactor):
    ctxFactory = certificate.getContextFactory(path.getDataPath())
    return endpoints.SSL4ClientEndpoint(reactor, "localhost", 4430, ctxFactory)
