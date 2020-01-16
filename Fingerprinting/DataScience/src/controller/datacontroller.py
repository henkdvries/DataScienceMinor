import os
import sys
import time
import itertools

import numpy as np

from tqdm import tqdm
from tabulate import tabulate
from multiprocessing import Pool

from tools.worker import Worker
from model.exercise import Exercise
from controller.foldercontroller import FolderController


class DataController():

    def __init__(self, config):
        """Class to convert data from excersises into sorted / filtered numpy array

        Arguments:
            config [confg] -- configuration file with specified settings.
        """
        self.config = config
        self.exercisedata = {}

    def run(self):
        """Runs all functions needed to sort / filter the exercises into a numpy array
        """
        self.load_from_files()
        self.filter_exercises()
        self.crossjoin_patient_exercise() 

        self.testdata = self.compute_numpy_data(self.test_combinationarray)
        self.traindata = self.compute_numpy_data(self.train_combinationarray)

        
    def start_timer(self):
        """starting time to record elapsed time.
        """
        self.start_time = time.time()

    def stop_timer(self):
        """Stopping the timer, could oly be done if the timer is started.
        Printing elapsed time.
        """
        if self.config.debug and self.start_time:
            end_time = time.time()
            timesum = end_time - self.start_time
            print('elapsed time:', timesum, 'seconds')

    def load_from_files(self):
        """Loads all data from CSV file, reads path from settings.
        """
        self.start_timer()

        if self.config.debug:
            print('Loading data from files')

        self.folders = [
            FolderController(os.path.join(self.config.basepath, 'alpha')),
            FolderController(os.path.join(self.config.basepath, 'bravo')),
            FolderController(os.path.join(self.config.basepath, 'charlie')),
            FolderController(os.path.join(self.config.basepath, 'delta')),
            FolderController(os.path.join(self.config.basepath, 'echo')),
        ]

    def filter_exercises(self):
        """Filters exercises into specific shape / order
        {
            <patientgroup> : {
                "alpha" : [<list of exercises>],
                "bravo" : [<list of exercises>],
                "charlie" : [<list of exercises>],
                "delta" : [<list of exercises>],
                "echo" : [<list of exercises>],
            },
            ... for each patientgroup
        }
        """
        if self.config.debug:
            print("Building dataset of file refrences")

        for catagorie in range(4):
            self.exercisedata[catagorie] = {}
            for group in range(5):
                name = Exercise.names[group]
                self.exercisedata[catagorie][name] = self.folders[group].filter_patientgroup(
                    catagorie + 1)

        if self.config.tables:
            print('Generating stats of all excersise groups')
            print()
            stats = []
            for catagorie, value in self.exercisedata.items():
                for excersise, filelist in value.items():
                    stats.append([excersise, catagorie + 1, len(filelist)])

            print(tabulate(stats, headers=[
                'excersise', 'Catagorie', 'Excersise Count']))
            print()

    def generate_patient_data(self, patientgroep, patientid):
        """Generates dictionary with all exercises filtered on patient id.
        Dictionary is sorted by exercise group:
        {
            "alpha": [<list of exercises>],
            "bravo": [<list of exercises>],
            "charlie": [<list of exercises>],
            "delta": [<list of exercises>],
            "echo": [<list of exercises>]
        }

        Arguments:
            patientgroep [dict] -- dictionary with all exercises of patients
            in specific patientgroup.
            patientid [int] -- id of patient to filter dictionary.

        Returns:
            [dict] -- list of exercises filtered by patientid.
        """
        patientdata = {}
        for name in Exercise.names:
            patientdata[name] = []

        for group, array in patientgroep.items():
            for excersise in array:
                if excersise.patient == patientid:
                    patientdata[group].append(excersise)

        return patientdata

    '''
    catagorie: 1 unique_patient_nummers: {1, 2, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 27, 28, 29}
    catagorie: 2 unique_patient_nummers: {1, 2, 3, 4, 6, 7, 8, 9, 11, 13, 15, 16, 17, 19, 21, 22, 23, 24, 25, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 40}
    catagorie: 3 unique_patient_nummers: {1, 4, 6, 7, 8, 11, 12, 15, 16, 17, 18, 19, 20, 21, 23, 24, 27, 28, 30, 31, 34, 35, 36, 39}
    catagorie: 4 unique_patient_nummers: {6, 11, 12, 13, 14, 15, 17, 20, 23, 24}
    '''

    def crossjoin_patient_exercise(self):
        """Finds all combinations possible between a single patient's exercises.
        Results from this process is stored in combinationarray.
        """

        test_filter = {
            0: [1, 5, 8, 13, 17, 20, 28],
            1: [4, 11, 15, 21, 25, 33, 39],
            2: [12, 19, 20, 31, 36],
            3: [1, 17, 23]
        }

        print('Crossjoining unique patient\'s exersises')
        print('max_chunck_size:', self.config.max_chunck_size)

        self.test_combinationarray = []
        self.train_combinationarray = []

        stats = []
        total_combinations = 0

        for catagorie in range(4):
            patientgroep = self.exercisedata[catagorie]

            unique_patient_nummers = set()
            for group, array in patientgroep.items():
                # getting a list of all patients id's
                unique = [x.patient for x in array if
                          x not in unique_patient_nummers and
                          unique_patient_nummers.add(x.patient) or True]

            if self.config.debug:
                print('catagorie:', catagorie + 1,
                      'unique_patient_nummers:', unique_patient_nummers)

            for patientnummer in unique_patient_nummers:
                patientdata = self.generate_patient_data(patientgroep,
                                                         patientnummer)
                # self.config.pp.pprint(patientdata)

                combinations = list(itertools.product(patientdata['alpha'],
                                                      patientdata['bravo'],
                                                      patientdata['charlie'],
                                                      patientdata['delta'],
                                                      patientdata['echo']))
                combinationresult = []
                if len(combinations) > self.config.max_chunck_size:
                    # Deviding to many combinations in multiple lists
                    # So it will be more even devided over workers
                    chunkcount = int(len(combinations) /
                                     self.config.max_chunck_size)
                    chunks = np.array_split(np.array(combinations), chunkcount)
                    # Size of all li objects must be the same as
                    # len(combinations)
                    for chunk in chunks:
                        if patientnummer in test_filter[catagorie]:
                            self.test_combinationarray.append(chunk)
                        else:
                            self.train_combinationarray.append(chunk)
                else:
                    if patientnummer in test_filter[catagorie]:
                        self.test_combinationarray.append(combinations)
                    else: 
                        self.train_combinationarray.append(combinations)

                if patientnummer in test_filter[catagorie]:
                    self.test_combinationarray.append(combinations)
                    
                patient_record_count = 0
                stats.append([catagorie + 1, patientnummer,
                              len(patientdata['alpha']),
                              len(patientdata['bravo']),
                              len(patientdata['charlie']),
                              len(patientdata['delta']),
                              len(patientdata['echo']),
                              int(len(combinations)), patientnummer in test_filter[catagorie]])
                total_combinations = total_combinations + len(combinations)

        print('Total combinations between unique patients:\t',
              total_combinations)

        if self.config.tables:
            print(tabulate(stats, headers=['catagorie', 'patientnummer',
                                           'alpha', 'bravo', 'charlie',
                                           'delta', 'echo',
                                           'possible combinations',
                                           'test person']))

    def compute_numpy_data(self, combinationarray):
        """Reshapes all exercise combinations into one numpy array.
        This is done by multiple workers configurable in main.py.

        Returns:
            [list] -- [2d np.array() with all filtered exercises,
                                    1d np.array() with fitting results]
        """
        data = np.empty((0, self.config.exercises * len(Worker.columns) *
                              Worker.frames_per_excersise))
        indicator = None
        
        print("Creating pool with [{size}] workers".format(
            size=self.config.workers))

        pool = Pool(self.config.workers)

        print("Generating np.array() from crossjoined patient exercises")
        for _ in tqdm(pool.imap_unordered(Worker.generate_exercises,
                                          combinationarray),
                      total=len(combinationarray)):
            pass

        print("Mapping results from workers....")
        values = pool.map(Worker.generate_exercises, combinationarray)

         
        print("Merging crossjoined patient exercises into main np.array()")
        for valueindex in tqdm(range(len(values))):
            np_patient_reshaped, patientgroup = values[valueindex]
            if np_patient_reshaped is not None and patientgroup is not None:
                if indicator is None:
                    indicator = np.copy(patientgroup)
                else:
                    indicator = np.append(indicator, patientgroup)
                data = np.append(data, np_patient_reshaped, axis=0)

        self.stop_timer()
        return [data, indicator]
