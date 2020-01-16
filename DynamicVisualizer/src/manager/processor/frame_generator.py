import numpy as np
from manager.processor.processor_interface import ProcessorInterface


class GenerateFrameProcessor(ProcessorInterface):
    def handle(self):
        np_combination_array = np.empty((0, len(self.config.columns) * self.config.frames_counts * self.config.frame_generator_count))
        for exercise_combination in self.data:
            # Creating empty array's
            data_array = [np.array([]) for _ in range(len(exercise_combination))]

            for exercise_id in range(len(exercise_combination)):
                for exercise_frame in exercise_combination[exercise_id].np_frames:
                    exercise_flat = exercise_frame.reshape(1, len(self.config.columns) * self.config.frames_counts)
                    data_array[exercise_id] = np.append(data_array[exercise_id], exercise_flat[0])

            for data in data_array:
                np_combination_array = np.vstack([np_combination_array, data])

        return np_combination_array
