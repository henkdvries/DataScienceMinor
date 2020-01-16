import os
from model.exercise import Exercise

import numpy as np
import pandas as pd
from tqdm import tqdm


class FolderController:

    def __init__(self, path, verbose=False):
        """Class in charge of a folder containing multiple exercises
        imports all the exercises into a list for later usage

        Arguments:
            path [string] -- path to exercise folder

        Keyword Arguments:
            verbose {bool} -- enables verbose mode, default is disabled
            (default: {False})

        Raises:
            FileExistsError: -- folder does not exists
        """
        # Saving path into class
        self.path = path
        self.data = None
        self.files = []
        self.indicator = None
        self.verbose = verbose

        print('FolderController()', self.path)

        # Checking if path exists
        if not os.path.exists(path):
            raise FileExistsError("Folder not found")
        else:
            self.import_files()

    def filter_patientgroup(self, catagorie):
        """filters all exercises in folder for a defined catagorie (patientgroup)

        Arguments:
            catagorie [int] -- number of catagorie (patientgroup)

        Returns:
            [list] -- list of all exercises in folder with a specific
            catagorie (patientgroup)
        """
        return [exercise for exercise in self.files
                if exercise.catagorie == catagorie]

    def import_files(self):
        """Function loops through defined folder in order to
        import all csv files as a Exercise
        """
        listdir = os.listdir(self.path)

        # Looping through all files in folder
        for i in tqdm(range(len(listdir))):
            f = listdir[i]
            if f.endswith('.csv'):
                if self.verbose:
                    print('importing file', f)
                # Creating a list of Parser objects to later read the data
                self.files.append(Exercise(os.path.join(self.path, f)))
