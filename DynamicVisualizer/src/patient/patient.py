import os
import re
from .exercise import Exercise
from config import config


class Patient:
    """
    Data housing for the exercises 
    Performed by a patient within a patientgroup
    """

    def __init__(self, path: str, load_other: bool):
        """
        :param str path: Path to the patient folder
        :param bool load_other: Load all but predefined exercises
        """
        self.path = path
        self.exercises = list()
        self.id = int(os.path.split(path)[1])
        self.__generate_exercise_list(load_other)

    def __generate_exercise_list(self, load_other: bool):
        """
        Generate exercise objects for the current patient

        :param bool load_other: Load all but predefined exercises
        """
        # Looping through files in patient folder
        for filename in os.listdir(self.path):
            # Checking if file is .csv
            if not filename.endswith('.csv'):
                continue

            # Verify the file is what we're looking for
            # NOTE: This should be changed if/when we introduce numbers into ex names
            _ex = re.findall(r'([a-z]+)', filename.split('.', 1)[0], re.IGNORECASE)[0]

            if _ex in config.exercisegroups:
                if not load_other:
                    self.exercises.append(Exercise(os.path.join(self.path, filename)))
            else:  # _ex not in exercisegroups
                if load_other:
                    self.exercises.append(Exercise(os.path.join(self.path, filename)))

    def get_exercises(self) -> list:
        return [exercise for exercise in self.exercises if exercise.exercisegroup in config().exercisegroups]

    def __iter__(self):
        self._index = -1
        return self

    def __next__(self):
        if self._index < len(self.exercises) - 1:
            self._index += 1
            return self.exercises[self._index]

        raise StopIteration

    def __str__(self):
        _id = re.findall(r'/(\d+)', self.path)[0]
        _exs = str()

        for e in self.exercises:
            _exs += re.findall(r'/(\w+)\.', e.path)[0] + ","
        _exs = _exs[:-1]

        return "Patient\n"\
            "-------\n"\
            "id: %s\n"\
            "exercises: %s" % (_id, _exs)
