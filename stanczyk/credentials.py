from clarent import certificate, path


def makeCredentials(email, namespace):
    """Creates credentials to connect to the exercise server.

    If the credentials already exist, raise

    """
    manhole = namespace["manhole"]

    manhole.overwriteLine("Creating credentials...")

    try:
        certificate.makeCredentials(path.getDataPath(), email)
    except IOError:
        manhole.overwriteLine("Credentials already exist!")
        return None

    manhole.overwriteLine("Successfully created credentials!")
