import pandas as pd
import numpy as np


class Worker:

    frames_per_excersise = 5
    columns = ["thorax_r_x", "thorax_r_y", "thorax_r_z",
               "clavicula_r_x", "clavicula_r_y", "clavicula_r_z",
               "scapula_r_x", "scapula_r_y", "scapula_r_z",
               "humerus_r_x", "humerus_r_y", "humerus_r_z",
               "ellebooghoek_r",
               "thorax_l_x", "thorax_l_y", "thorax_l_z",
               "clavicula_l_x", "clavicula_l_y", "clavicula_l_z",
               "scapula_l_x", "scapula_l_y", "scapula_l_z",
               "humerus_l_x", "humerus_l_y", "humerus_l_z",
               "ellebooghoek_l"]

    @staticmethod
    def select_rows(rowcount, numrows):
        """creates a list of evenly devided row indexes based on size of an table.

        Arguments:
            rowcount [int] -- amount of rows in the table.
            numrows [int] -- number of rows to devide in.

        Returns:
            [list] -- list of row indexes based on size of table.
        """
        rows = []
        for index in range(1, numrows):
            rows.append(int((rowcount / numrows) * index))
        rows.append(int((rowcount / numrows) * numrows) - 1)

        return rows

    @staticmethod
    def generate_exercises(patient_combinations):
        """Creates two numpy array with all computed patient exercises
        and patient group as indicator.

        Arguments:
            patient_combinations [list] --
            list of multiple patient exercise combinations.

        Returns:
            [numpy.array, numpy.array] -- list of all computed patients
            as rows in a numpy array, list of patiengroups as numpy array.
            Same order as the patient rows.
        """
        np_patient_reshaped = np.empty((0, 5 *
                                        len(Worker.columns) *
                                        Worker.frames_per_excersise))

        indicator = None
        for combination in patient_combinations:
            exercise_array, patientgroup = Worker.reshape_exercises(
                combination)

            if indicator is None:
                indicator = np.array([patientgroup])
            else:
                indicator = np.append(indicator, [patientgroup])
            np_patient_reshaped = np.append(
                np_patient_reshaped, [exercise_array], axis=0)
        return [np_patient_reshaped, indicator]

    @staticmethod
    def reshape_exercises(args):
        """creates one row of [5 * columns * frames] columns for one exercise combination.

        Arguments:
            args [list] -- list with one exercise combination
            [alpha, bravo, charlie, delta, echo].

        Returns:
            [numpy.array, int] -- row with combined exercise frames (650 columns),
            int with patientgroup of exercise combination.
        """
        # Create dataframe object here
        # args contain alpha, bravo, charlie, delta, echo

        # exercise_array = np.empty(
        #     [0, len(Worker.columns) *
        #         len(args) *
        #         Worker.frames_per_excersise])

        exercise_array = np.array([])

        patientgroup = args[0].catagorie
        for exercise in args:  # Alpha Bravo Charlie Delta Echo
            row_selection = Worker.select_rows(
                exercise.dataframe_size(), Worker.frames_per_excersise)

            np_exercise = exercise.dataframe[Worker.columns].to_numpy()
            for rowindex in row_selection:
                exercise_array = np.append(
                    exercise_array, np_exercise[rowindex])
        return [exercise_array, patientgroup]
