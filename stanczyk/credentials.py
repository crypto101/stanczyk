from clarent import certificate, path


def makeCredentials(email, namespace):
    """Creates new credentials for connecting to the Crypto 101 exercise
    servers.

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
