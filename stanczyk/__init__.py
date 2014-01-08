from stanczyk._version import __version__
version = __version__

from stanczyk.exercises import getExercises, getExerciseDetails
from stanczyk.protocol import connect
from stanczyk.proxy import connectProxy
consoleFunctions = [
    connect,
    getExercises,
    getExerciseDetails,
    connectProxy
]
