import itertools
from manager.processor.processor_interface import ProcessorInterface


class GenerateCombinationsProcessor(ProcessorInterface):
    def handle(self):
        patient_data = {}
        for exercisegroup in self.config.exercisegroups:  # Loop through AF, EL, AB, etc...
            patient_data[exercisegroup] = []

            for exercise in self.data:  # loop through all exercises for the current patient
                # checking each exercise's name, compare it with the current exercise group

                if exercise.exercisegroup != exercisegroup:
                    continue

                # Adding the exercise to the correct group
                # If name is correct
                patient_data[exercisegroup].append(exercise)

        # Calculating all combinations based on exercise groups
        return list(itertools.product(*[patient_data[ex_group] for ex_group in self.config.exercisegroups]))
        return list(itertools.product(patient_data['AF'], patient_data['EL'], patient_data['AB'],
                                      patient_data['RF'], patient_data['EH']))
