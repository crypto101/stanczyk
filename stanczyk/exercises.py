from clarent.exercise import GetExercises, GetExerciseDetails
from stanczyk.util import _getRemote
from texttable import Texttable


def getExercises(namespace, solved=False):
    """Gets some exercises that are currently avaialble to you.

    """
    d = _getRemote(namespace).callRemote(GetExercises, solved=solved)
    d.addCallback(_displayExercisesTable, namespace)

    return None


def _displayExercisesTable(response, namespace):
    """Builds a table of the available exercises and prints it to the
    terminal.

    """
    table = Texttable()
    table.header(["Identifier", "Title"])
    for exercise in response["exercises"]:
        table.add_row([repr(exercise["identifier"]), exercise["title"]])

    manhole = namespace["manhole"]

    tableText = table.draw().encode("utf-8")
    manhole.overwriteLine("{}".format(tableText))


def getExerciseDetails(identifier, namespace):
    """Shows the detailed description of a particular excerise.

    """
    remote = _getRemote(namespace)
    d = remote.callRemote(GetExerciseDetails, identifier=identifier)
    d.addCallback(_displayExerciseDetails, namespace)

    return None


def _displayExerciseDetails(response, namespace):
    """Write the exercise details to the console.

    """
    title = response["title"]
    line = "=" * len(title)
    header = "\n".join([line, title, line])

    content = "\n\n" + header + "\n\n" + response["description"]
    namespace["manhole"].overwriteLine(content.encode("utf-8"))
