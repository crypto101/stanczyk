from stanczyk._version import __version__
version = __version__

from stanczyk.credentials import makeCredentials
from stanczyk.exercises import getExercises, getExerciseDetails
from stanczyk.protocol import connect
from stanczyk.proxy import connectProxy
consoleFunctions = [
    makeCredentials,
    connect,
    getExercises,
    getExerciseDetails,
    connectProxy
]
