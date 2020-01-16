from manager.processor import *

from config import config 


class DataManager:

    processed_data = dict()

    def __init__(self, *args):
        """
        :param args: categories to load
        :param config: Machine learning configuration
        """
        ProcessorRules(config())  # Verify the given configuration

        self.categories = args

    def generate_pipeline(self) -> list:
        """
        Generate a processing pipeline
        based on the given configuration

        :return: processor pipeline
        :rtype: list
        """
        pipeline = list()
        if config().occupied_space:
            pipeline.append(OccupiedSpaceProcessor)
            return pipeline

        pipeline.append(GenerateCombinationsProcessor)

        if config().frame_generator:
            pipeline.append(GenerateFrameProcessor)
        else:
            pipeline.append(DataFinalizationProcessor)

        return pipeline

    def send_through(self, *args):
        """
        Send the patient's exercises through the
        Specified processors. Results will be written
        Into <pat obj>.processed

        :param args: Processors
        """
        for cat in self.categories:
            self.processed_data[str(cat.id)] = dict()
            for pat in cat:
                self.processed_data[str(cat.id)][str(pat.id)] = pat.get_exercises()
                for processor in args:
                    self.processed_data[str(cat.id)][str(pat.id)] = (
                        processor(
                            self.processed_data[str(cat.id)][str(pat.id)],
                            config
                        )
                    ).handle()
