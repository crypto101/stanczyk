from clarent import certificate
from clarent.path import getDataPath
from stanczyk.credentials import makeCredentials
from stanczyk.test.util import CommandTestMixin
from twisted.trial.unittest import SynchronousTestCase


class MakeCredentialsTests(CommandTestMixin, SynchronousTestCase):
    def test_makeCredentials(self):
        """The makeCredentials command can be used to make credentials. It
        displays helpful messages along the way.

        """
        self.patch(certificate, "makeCredentials", self._fakeMakeCredentials)
        makeCredentials("test@example.com", self.namespace)
        self.assertEqual(self.manhole.line, "Successfully created credentials!")


    def _fakeMakeCredentials(self, path, email):
        """Pretend to have make some credentials.

        Checks that the user is being notified that credentials are
        being made (this can take a non-trivial amount of time).
        Checks that the correct path is being passed. Checks that the
        correct e-mail is being passed.

        """
        self.assertEqual(self.manhole.line, "Creating credentials...")
        self.assertEqual(path, getDataPath())
        self.assertEqual(email, "test@example.com")


    def test_credentialsAlreadyExist(self):
        """If the credentials already existed, a useful error message is
        displayed.

        """
        self.patch(certificate, "makeCredentials", self._failToMakeCredentials)
        makeCredentials("test@example.com", self.namespace)
        self.assertEqual(self.manhole.line, "Credentials already exist!")


    def _failToMakeCredentials(self, path, email):
        """Pretend to fail to make some credentials.

        """
        self._fakeMakeCredentials(path, email)
        raise IOError("whatever")
