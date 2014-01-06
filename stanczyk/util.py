"""
Utilities that don't fit well anywhere else.
"""
def _getRemote(namespace):
    """Gets the remote protocol, or raises an error.

    This is intended to be used by command implementations.

    This isn't implemented as an argument-injecting decorator, because
    the console code uses introspection to tell users how to call
    console commands.

    """
    try:
        return namespace["remote"]
    except KeyError:
        raise RuntimeError("You are not connected to the exercise server. "
                           "Call ``connect``.")
