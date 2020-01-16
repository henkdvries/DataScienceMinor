import numpy as np
from manager.processor.processor_interface import ProcessorInterface


class DataFinalizationProcessor(ProcessorInterface):
    def handle(self):
        np_combination_array = np.empty((0, len(self.config.columns) *
                                         self.config.frames_counts * self.config.exercise_count))

        for exercise_combination in self.data:
            data = np.array([])
            for exercise in exercise_combination:
                # Getting 5 frames from exercise
                exercise_flat = exercise.np_data.reshape(1, len(self.config.columns) * self.config.frames_counts)
                data = np.append(data, exercise_flat[0])

            np_combination_array = np.vstack([np_combination_array, data])

        return np_combination_array
