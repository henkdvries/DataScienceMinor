from multiprocessing import freeze_support
from tabulate import tabulate
from tools.configloader import ConfigLoader, ConfigCreator
from patient.patientgroup import PatientGroup
from config import config
from data import run_model, run_original
from tools.visualis import Visualize 

from manager.data import DataManager
from manager.train_test import TrainTestManager
from tools.stats import print_group_stats
import tabulate
import os
import json
import numpy as np

# loader = ConfigCreator()
# loader.create_configurations()
# exit()



print('process started with pid:', os.getpid())

# Importing patient groups
patient_groups = [
    PatientGroup(config.basepath.format(groupid=1)),
    PatientGroup(config.basepath.format(groupid=2)),
    PatientGroup(config.basepath.format(groupid=3)),
    # PatientGroup(config.basepath.format(groupid=4)),
]

# Loading a list of configurations 
configloader = ConfigLoader(patient_groups, 'bestandworstconfigs.json')
# configloader = ConfigLoader(patient_groups, 'test_config.json')

if __name__ == "__main__":
    freeze_support()
    configloader.clear_evaluation_result()
    i = 1
    # TODO: Calculate time between runs
    while configloader.next_config():
        
        print(i)
        print('Updating exercises based on config... ')
        configloader.update_exercises()

        dm = DataManager(*configloader.patient_groups)
        pipeline = dm.generate_pipeline()
        print("Based on the above configuration the following "
              "pipeline is created %s " % pipeline)
        dm.send_through(*pipeline)

        train, test = (TrainTestManager(patient_groups)).create_split()
        trainX, trainy = train 
        testX, testy = test 
        
        if config.normalise: 
            trainX = (trainX % 360) / 360 
            testX = (testX % 360) / 360 
      
        print('Running the model....')
        score = run_model([trainX, trainy, testX, testy], i)
        uniqueval, occurCount = np.unique(trainy,return_counts=True)
        print(uniqueval)
        print(occurCount)

        uniqueval, occurCount = np.unique(testy,return_counts=True)
        print(uniqueval)
        print(occurCount)
        print('return counter value, current value {}'.format(i))
        i = configloader.update_table(score)
        print(i)

        print(score['Accuracy'])



    print('Finished running all configurations')
    configloader.print_table()


#   Accuracy       MCC    LogLoss      RSME     RMSLE  default
# ----------  --------  ---------  --------  --------  ---------
#   0.889488  0.752936    3.16644  0.894728  0.272647  True
#   0.731449  0.642798    3.45956  0.755038  0.224504  True
