from stanczyk._version import __version__
version = __version__

from stanczyk.protocol import connect
from stanczyk.proxy import connectProxy
consoleFunctions = [connect, connectProxy]
