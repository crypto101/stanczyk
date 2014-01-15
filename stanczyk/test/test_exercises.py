from clarent.exercise import GetExercises
from stanczyk.exercises import getExercises
from stanczyk.test.util import CommandTests


EXPECTED_TABLE = """
+------------+-----------+
| Identifier |   Title   |
+============+===========+
| 'one'      | Title one |
+------------+-----------+
| 'two'      | Title two |
+------------+-----------+
""".strip()



class GetExercisesTests(CommandTests):
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
