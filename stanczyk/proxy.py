from twisted.internet import endpoints, reactor
from txampext.multiplexing import ProxyingFactory


def connectProxy(identifier, namespace, reactor=reactor):
    """Proxy connections server with the given identifier.

    """
    remote = namespace.get("remote")
    if remote is None:
        raise RuntimeError("You are not connected to the exercise server. "
                           "Call ``connect``.")

    factory = ProxyingFactory(remote, identifier)
    endpoint = endpoints.TCP4ServerEndpoint(reactor, 0, interface="localhost")
    d = endpoint.listen(factory)

    d.addCallback(_listening, namespace=namespace)
    return d



def _listening(listeningPort, namespace):
    """Started listening; report success to terminal.

    """
    return listeningPort # TODO: Report success
