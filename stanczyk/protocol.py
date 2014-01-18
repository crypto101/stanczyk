from clarent import certificate, exercise, path
from twisted.internet import protocol, reactor
from twisted.internet.endpoints import SSL4ClientEndpoint
from twisted.protocols import amp
from txampext import multiplexing


class Protocol(multiplexing.ProxyingAMPLocator, amp.AMP):
    """Stanczyk's client AMP protocol.

    """
    @property
    def namespace(self):
        return self.factory.namespace


    @exercise.NotifySolved.responder
    def notifySolved(self, identifier, title):
        """Notifies the user that they have completed an exercise.

        """
        line = (u"\nCongratulations! You have solved the {} excercise ({})."
                .format(identifier, title).encode("utf-8"))
        self.namespace["manhole"].overwriteLine(line)
        return {}



class Factory(protocol.ReconnectingClientFactory):
    """A factory that will reconnect (with exponential backoff).

    """
    protocol = Protocol

    def __init__(self, namespace):
        self.namespace = namespace



def connect(namespace, _reactor=reactor):
    """Connect to the exercise server.

    """
    if "remote" in namespace:
        raise RuntimeError("You're already connected.")

    try:
        endpoint = _makeEndpoint(_reactor)
    except IOError:
        namespace["manhole"].overwriteLine("Couldn't find your credentials. "
                                           "Did you call 'makeCredentials'?")
        return None

    d = endpoint.connect(Factory(namespace))
    d.addCallback(_storeRemote, namespace=namespace)

    return None # don't return the deferred, or the REPL will display it


def _storeRemote(remote, namespace):
    """Stores the remote in the namespace; reports success to console.

    """
    namespace["remote"] = remote
    namespace["manhole"].overwriteLine("Connected to the exercise server!")


def _makeEndpoint(reactor):
    """Creates a suitable endpoint with the given reactor.

    Uses clarent to create a context factory using the default data
    path, and then creates a SSL client endpoint with that context
    factory.

    """
    ctxFactory = certificate.getContextFactory(path.getDataPath())
    return SSL4ClientEndpoint(reactor, "localhost", 4430, ctxFactory)
