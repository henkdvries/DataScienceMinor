from manager.data import DataManager
from sklearn.utils import shuffle
from config import config
import numpy as np


class TrainTestManager:
    def __init__(self, categories):
        self.categories = categories

    def create_split(self) -> ((np.ndarray, np.ndarray), (np.ndarray, np.ndarray)):
        """
        Create traditional split based on
        specified patients per category

        :return: train and test data
        :rtype: tuple
        """
        cat_pat = dict()
        for cat in self.categories:
            cat_pat[cat] = config.test_patients[str(cat.id)]

        train, test = self.generate_data(cat_pat, invert=True), self.generate_data(cat_pat)

        if config.shuffle_train:
            train = self.shuffle_data(*train)

        if config.batch_size > 0:
            train = self.batch_split(*train)

        return train, test

    def create_percentage_based_split(self) -> ((list, list), (list, list)):
        """
        Create percentage based split

        :return: train and test data
        :rtype: tuple
        """
        cat_pat = dict()
        for cat in self.categories:
            cat_pat[cat] = list()
            total = cat.n_samples()
            print("Total of %i samples in group" % total)
            partial = total * config.train
            delta = -partial

            for pat in cat:
                cat_pat[cat].append(pat.id)
                print("Adding patient %s to train" % pat.id)
                delta += len(pat.processed)
                print("Current delta %i" % delta)
                if delta >= 0:
                    break

        return self.generate_data(cat_pat), self.generate_data(cat_pat, True)

    def validation_data(self, data: list, indicator: list) -> ((list, list), (list, list)):
        """
        Create a validation split from the train data

        :param list data: data used to train the model
        :param list indicator: data true value
        :return: train and validation data split
        :rtype: tuple
        """
        index = int(len(data) * (config.validation_split/100))

        return (data[:index], indicator[:index]), (data[index:], indicator[index:])

    def batch_split(self, data: list, indicator: list) -> [(list, list), ...]:
        """
        Create train batches for partial learning

        :param list data: data used to train model
        :param indicator: data true value
        :return: data in the given batch size
        :rtype: tuple
        """

        # data and indicator cannot differ in size
        # therefor we don't define step size individually
        steps = range(config.batch_size, len(data), config.batch_size)
        data_batches = np.zeros(shape=(len(steps),), dtype=object)
        indicator_batches = np.zeros(shape=(len(steps),), dtype=object)

        prev = 0
        batch_index = 0
        for i in steps:
            data_batches[batch_index] = data[prev:i]
            indicator_batches[batch_index] = indicator[prev:i]

            prev = i
            batch_index += 1

        return data_batches, indicator_batches

    def shuffle_data(self, data: list, indicator: list) -> (list, list):
        """
        Facade for sklearn's shuffle method

        :param list data: data used to train/test model
        :param list indicator: data true value
        :return: shuffled data with their respective indicator
        :rtype: tuple
        """
        return shuffle(data, indicator)

    def generate_data(self, mapping: dict, invert=False) -> (np.ndarray, np.ndarray):
        """
        Create data and indicator set based
        on the given dictionary.
        Struct should be {<PatientGroup>: [patient ids]}

        :param dict mapping: data to process
        :param bool invert: include or exclude the listed patients
        :return: data and their respective indicator
        :rtype: tuple
        """
        data = list()
        indicator = list()

        if not invert:
            for cat in mapping.keys():
                for pat in mapping[cat]:
                    try:
                        data.extend(DataManager.processed_data[str(cat.id)][str(pat)])
                        indicator.extend([cat.id] * len(DataManager.processed_data[str(cat.id)][str(pat)]))
                    except KeyError:
                        print("patient %i does not exist in category %i" % (pat, cat.id))
                        continue
        else:
            for cat in mapping.keys():
                for pat in cat:
                    if pat.id in mapping[cat]:
                        continue
                    try:
                        data.extend(DataManager.processed_data[str(cat.id)][str(pat.id)])
                        indicator.extend([cat.id] * len(DataManager.processed_data[str(cat.id)][str(pat.id)]))
                    except KeyError:
                        print("patient %i does not exist in category %i" % (pat.id, cat.id))
                        continue

        return np.array(data), np.array(indicator)
