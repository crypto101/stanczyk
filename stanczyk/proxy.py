from stanczyk.util import _getRemote
from twisted.internet import endpoints, reactor
from txampext.multiplexing import ProxyingFactory


def connectProxy(identifier, namespace, _reactor=reactor):
    """Creates a virtual connection to a server.

    """
    endpoint = endpoints.TCP4ServerEndpoint(_reactor, 0, interface="localhost")
    factory = ProxyingFactory(_getRemote(namespace), identifier)
    d = endpoint.listen(factory)
    d.addCallback(_listening, namespace, identifier)
    return None


def _listening(listeningPort, namespace, identifier):
    """Started listening; report success to terminal.

    """
    host = listeningPort.getHost()
    template = "{id} is now listening on {h.host}:{h.port}"
    namespace["manhole"].overwriteLine(template.format(h=host, id=identifier))
