from clarent.exercise import GetExercises, GetExerciseDetails
from stanczyk.exercises import getExercises, getExerciseDetails
from stanczyk.test.util import ConnectedCommandTestMixin
from twisted.trial.unittest import SynchronousTestCase


EXPECTED_TABLE = """
+------------+-----------+
| Identifier |   Title   |
+============+===========+
| 'one'      | Title one |
+------------+-----------+
| 'two'      | Title two |
+------------+-----------+
""".strip()


EXPECTED_DETAILS = """

=====
Title
=====

The description.
""".rstrip()



class GetExercisesTests(ConnectedCommandTestMixin, SynchronousTestCase):
    command = staticmethod(getExercises)

    def test_getExercises(self):
        """The exercise getting command gets unsovled exercises by default,
        and then pretty-prints them to the terminal. It returns None.

        """
        result = getExercises(self.namespace)
        self.assertIdentical(result, None)

        self.assertEqual(self.remote.command, GetExercises)
        self.assertEqual(self.remote.kwargs, {"solved": False})

        self.remote.deferred.callback({"exercises": [
            {"identifier": "one", "title": u"Title one"},
            {"identifier": "two", "title": u"Title two"}
        ]})
        self.assertEqual(self.manhole.line, EXPECTED_TABLE)


    def test_getSolvedExercises(self):
        """The exercise getting command passes its "solved" parameter in the
        remote GetExercises call.

        """
        getExercises(self.namespace, solved=True)

        self.assertEqual(self.remote.command, GetExercises)
        self.assertEqual(self.remote.kwargs, {"solved": True})



class GetExerciseDetailsTests(ConnectedCommandTestMixin, SynchronousTestCase):
    command = staticmethod(getExerciseDetails)
    kwargs = {"identifier": "xyzzy"}

    def test_getExerciseDetails(self):
        """The exercise detail getting command gets the details of the
        exercise specified by identifier. It pretty-prints the result
        to the terminal. It returns None.

        """
        identifier, title, description = "xyz", "Title", "The description."

        result = getExerciseDetails(identifier, namespace=self.namespace)
        self.assertIdentical(result, None)

        self.assertEqual(self.remote.command, GetExerciseDetails)
        self.assertEqual(self.remote.kwargs, {"identifier": identifier})

        self.remote.deferred.callback({
            "identifier": identifier,
            "title": title,
            "description": description
        })
        self.assertEqual(self.manhole.line, EXPECTED_DETAILS)
