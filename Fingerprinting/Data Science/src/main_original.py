import os
import sys
import time
import pprint
import itertools

import numpy as np
import pandas as pd

from tqdm import tqdm
from tabulate import tabulate

from sklearn import preprocessing
from sklearn.metrics import classification_report, accuracy_score
from sklearn.model_selection import train_test_split

from multiprocessing import Pool
from multiprocessing import Process, freeze_support

from ml.logisticregression import LogisticRegressionModel
from controller.foldercontroller import FolderController
from model.exercise import Exercise
from tools.worker import Worker

start_time = time.time()

class config:
    debug = True
    pp = pprint.PrettyPrinter(indent=4)
    exercises = 5
    workers = 20
    max_chunck_size = 100

    test_size = 0.2
    test_random_state = 42

    if debug:
        basepath = "src/data/cleaned-regrouped-small"
    else:
        basepath = "src/data/cleaned-regrouped"

 


#########

print('ORTHO: Prepairing Dataset')
foldercontrollers = [
    FolderController(os.path.join(config.basepath, 'alpha')),
    FolderController(os.path.join(config.basepath, 'bravo')),
    FolderController(os.path.join(config.basepath, 'charlie')),
    FolderController(os.path.join(config.basepath, 'delta')),
    FolderController(os.path.join(config.basepath, 'echo'))]

if config.debug:
    print("Building dataset of file refrences")

data = {}
for catagorie in range(4):
    data[catagorie] = {}
    for group in range(5):
        name = Exercise.names[group]
        data[catagorie][name] = foldercontrollers[group].filter_patientgroup(
            catagorie + 1)


if config.debug:
    print('Generating stats of all excersise groups')
    print()
    stats = []
    for catagorie, value in data.items():
        for excersise, filelist in value.items():
            stats.append([excersise, catagorie + 1, len(filelist)])

    print(tabulate(stats, headers=[
          'excersise', 'Catagorie', 'Excersise Count']))
    print()


def generate_patient_data(patientgroep, patientid):
    patientdata = {}
    for name in Exercise.names:
        patientdata[name] = []

    for group, array in patientgroep.items():
        for excersise in array:
            if excersise.patient == patientid:
                patientdata[group].append(excersise)

    return patientdata


print('Crossjoining unique patient\'s exersises')
print('max_chunck_size:', config.max_chunck_size)

stats = []
total_combinations = 0
combinationarray = []

for catagorie in range(4):
    patientgroep = data[catagorie]

    unique_patient_nummers = set()
    for group, array in patientgroep.items():
        # getting a list of all patients id's
        unique = [x.patient for x in array if
                  x not in unique_patient_nummers and
                  unique_patient_nummers.add(x.patient) or True]

    if config.debug:
        print('catagorie:', catagorie + 1,
              'unique_patient_nummers:', unique_patient_nummers)

    for patientnummer in unique_patient_nummers:
        patientdata = generate_patient_data(patientgroep, patientnummer)
        config.pp.pprint(patientdata)

        combinations = list(itertools.product(patientdata['alpha'],
                                              patientdata['bravo'],
                                              patientdata['charlie'],
                                              patientdata['delta'],
                                              patientdata['echo']))

        if len(combinations) > config.max_chunck_size:
            # Deviding to many combinations in multiple lists
            # So it will be more even devided over workers
            chunkcount = int(len(combinations) / config.max_chunck_size)
            chunks = np.array_split(np.array(combinations), chunkcount)
            # Size of all li objects must be the same as len(combinations)
            for chunk in chunks:
                combinationarray.append(chunk)
        else:
            combinationarray.append(combinations)

        patient_record_count = 0
        stats.append([catagorie + 1, patientnummer,
                      len(patientdata['alpha']),
                      len(patientdata['bravo']),
                      len(patientdata['charlie']),
                      len(patientdata['delta']),
                      len(patientdata['echo']),
                      int(len(combinations)), patient_record_count])
        total_combinations = total_combinations + len(combinations)

print('Total combinations between unique patients:\t', total_combinations)

if config.debug:
    print(tabulate(stats, headers=['catagorie', 'patientnummer',
                                   'alpha', 'bravo', 'charlie',
                                   'delta', 'echo',
                                   'possible combinations', 'total rows']))
    print('Array size:', sys.getsizeof(combinationarray),
          'shape', len(combinationarray))

# Creating 2d array with correct number of columns
np_main = np.empty((0, config.exercises * len(Worker.columns) *
                    Worker.frames_per_excersise))


print("Creating pool with [{size}] workers".format(size=config.workers))

pool = Pool(config.workers)

print("Generating np.array() from crossjoined patient exercises")
for _ in tqdm(pool.imap_unordered(Worker.generate_exercises, combinationarray),
              total=len(combinationarray)):
    pass

print("Mapping results from workers....")
values = pool.map(Worker.generate_exercises, combinationarray)
 
indicator = None
print("Merging crossjoined patient exercises into main np.array()")
for valueindex in tqdm(range(len(values))):
    np_patient_reshaped, patientgroup = values[valueindex]
    if np_patient_reshaped is not None and patientgroup is not None:
        if indicator is None:
            indicator = np.copy(patientgroup)
        else:
            indicator = np.append(indicator, patientgroup)
        np_main = np.append(np_main, np_patient_reshaped, axis=0)

    # maindataframe = maindataframe.append(excersise_series, ignore_index=True)

# TODO: Balancing data-set checking amount of records per patiengroup

end_time = time.time()
timesum = end_time-start_time
print("Finished creating dataset!")
print('time:', timesum, 'seconds')
print('shape:', np_main.shape)
print('indicator:', indicator.shape)
print()
print('ORTHO: Training MachineLearning Model')
print()

print("Preprocessing: scale")
X_scaled = preprocessing.scale(np_main)

print("Splitting dataset: {min}/{max} randomstate: {random}".format(
    min=config.test_size, max=1-config.test_size,
    random=config.test_random_state))

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, indicator, test_size=config.test_size,
    random_state=config.test_random_state)
 
logisticregression = LogisticRegressionModel()
print("Training started")
logisticregression.train(X_train, y_train)

print("Finished Training")

y_pred = logisticregression.predict(X_test)
print(classification_report(y_test, y_pred, digits=3))
print(accuracy_score(y_test, y_pred, normalize=True, sample_weight=None))
end_time = time.time()
timesum = end_time-start_time

print('time:', timesum, 'seconds')
exit()
