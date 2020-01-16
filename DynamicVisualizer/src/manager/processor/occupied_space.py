import tools.eulerspace
from patient.exercise import Exercise
from manager.processor.processor_interface import ProcessorInterface


class OccupiedSpaceProcessor(ProcessorInterface):
    def handle(self):
        processed = list()

        for exercise in self.data:
            # define the axes of a 3d space for every bone
            exercise.space3dAxis = []
            for i in (0, 3, 6, 9, 15, 18, 21, 24):
                if ((Exercise.columns[i] in self.config.columns) and
                        (Exercise.columns[i + 1] in self.config.columns) and
                        (Exercise.columns[i + 2] in self.config.columns)):
                    exercise.space3dAxis.append(
                        (Exercise.columns[i], Exercise.columns[i + 1], Exercise.columns[i + 2]))

            flattened_data = list()
            for i, ax in enumerate(exercise.space3dAxis):
                dat = tools.eulerspace.def_space(exercise, ax)
                flattened_data.extend(dat.ravel())

            processed.append(flattened_data)

        return processed
