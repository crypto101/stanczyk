from twisted.internet import endpoints, reactor
from txampext.multiplexing import ProxyingFactory


def connectProxy(identifier, namespace, reactor=reactor):
    """Start listening on some free local port; connections will be
    proxied to the virtual server with the given identifier.

    """
    remote = namespace.get("remote")
    if remote is None:
        raise RuntimeError("You are not connected to the exercise server. "
                           "Call ``connect``.")

    factory = ProxyingFactory(remote, identifier)
    endpoint = endpoints.TCP4ServerEndpoint(reactor, 0, interface="localhost")
    d = endpoint.listen(factory)
    d.addCallback(_listening, identifier, namespace)
    return None


def _listening(listeningPort, identifier, namespace):
    """Started listening; report success to terminal.

    """
    host = listeningPort.getHost()
    template = "{id} is now listening on {h.host}:{h.port}"
    namespace["manhole"].writeLine(template.format(h=host, id=identifier))
