import tqdm
import itertools
import numpy as np 
from tabulate import tabulate
import datetime

from patient.patientgroup import PatientGroup
import matplotlib.pyplot as plt
from models.models import Models
from models.logisticregression import LogisticRegressionModel 
from models.svc import SVCModel 
from models.mlpclassifier import MLPClassifierModel
from multiprocessing import Process, freeze_support
from pprint import pprint 

from tools.configloader import ConfigLoader, ConfigCreator
from config import config


def run_model(data, counter):

    # data = [train[0], train[1], test[0], test[1]]
    if config.model == Models.LOGISTIC_REGRESSION: 
        model = LogisticRegressionModel(data, solver="lbfgs", max_iter=2000, multi_class="auto")
    elif config.model == Models.SVC:  model = SVCModel(data, config, gamma="auto")
    elif config.model == Models.MLPCLASSIFIER: model = MLPClassifierModel(data, config,solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, ), random_state=1)
    else:  raise ValueError("No model is set in the configuration")

    model.train()
    metrics = model.retrieve_metrics()
    x = model.plot_conf_matrix()
    plt.savefig('C:\\Users\\lennart\Desktop\\results\\{}\\figuur{}.png'.format(counter, counter))
    del(model)
    return metrics


def generate_data(combinations):
    np_combination_array = np.empty((0,len(config.columns) * config.frames_counts * config.exercise_count))
    np_indicator_array = np.array([]) 
    for exercise_combination in tqdm.tqdm(combinations): 
        data = np.array([]) 
        for exercise in exercise_combination: 
            exercise_flat = exercise.np_data.reshape(1, len(config.columns) * config.frames_counts)
            data = np.append(data, exercise_flat[0])

        np_combination_array = np.vstack ([np_combination_array, data])
        np_indicator_array = np.append(np_indicator_array, exercise_combination[0].patientgroup)

    return np_combination_array, np_indicator_array


def run_original(patient_groups):
    test_combinations = list()
    train_combinations = list()
    table_data = []

    for patientgroup in patient_groups:
        for patient in patientgroup:  
            patient_data = {}
            for exercisegroup in config.exercisegroups: 
                patient_data[exercisegroup] = [] 
                for exercise in patient:  
                    if exercise.exercisegroup == exercisegroup: 
                        patient_data[exercisegroup].append(exercise)

            patient_groups = [value for key, value in patient_data.items()]
            resultaten = list(itertools.product(*patient_groups))
            
            if len(resultaten) > 0:
                patient_nr = int(patient.exercises[0].patientid)
                patientgroup = patient.exercises[0].patientgroup
                if len(patient.exercises) > 0:
                    if int(patient.exercises[0].patientid) in config.test_patients[patient.exercises[0].patientgroup]:
                        test_combinations.extend(resultaten)
                    else: 
                        train_combinations.extend(resultaten)

    np_combination_test, np_indicator_test = generate_data(test_combinations)
    np_combination_train, np_indicator_train = generate_data(train_combinations)

    return (np_combination_train, np_indicator_train), (np_combination_test, np_indicator_test)



# def run_original(patient_groups):
#     test_combinations = list()
#     train_combinations = list()
#     table_data = []

#     for patientgroup in patient_groups:
#         for patient in patientgroup:  # loop through all patients within a patientgroup
#             patient_data = {}
#             for exercisegroup in config.exercisegroups:
#                 # Loopen door AF, EL, AB, etc...
#                 patient_data[exercisegroup] = []

#                 # Looping through all exercises of patient
#                 for exercise in patient:  # loop through all exercises for the current patient
#                     # checking each exercise's name, compaire it with
#                     # the current exercise group
#                     if exercise.exercisegroup == exercisegroup:
#                         # Adding the exercise to the correct group
#                         # If name is correct
#                         patient_data[exercisegroup].append(exercise)

#             # Calculating all combinations based on exercise gruops
#             patient_groups = [value for key, value in patient_data.items()]

#             resultaten = list(itertools.product(*patient_groups))
            
#             if len(resultaten) > 0:
#                 patient_nr = int(patient.exercises[0].patientid)
#                 patientgroup = patient.exercises[0].patientgroup

#                 # table_data.append([
#                 #     patientgroup, patient_nr,
#                 #     len(patient_data['AF']), len(patient_data['EL']), len(patient_data['AB']),
#                 #     len(patient_data['RF']), len(patient_data['EH']), len(resultaten),
#                 #     patient_nr in config.test_patients[patientgroup]])

#                 if len(patient.exercises) > 0:
#                     if int(patient.exercises[0].patientid) in config.test_patients[patient.exercises[0].patientgroup]:
#                         test_combinations.extend(resultaten)
#                     else: 
#                         train_combinations.extend(resultaten)
#     if config.logging:
#         print(tabulate.tabulate(table_data, headers=[
#             'catagorie', 'patientnummer', 'AF', 'EL', 'AB',
#             'RF', 'EH', 'combinations', 'test person']))

    
#     print('train_combinations: ', len(train_combinations))
#     print('test_combinations: ', len(test_combinations))


#     def generate_data_new(combinations):
#         np_combination_array = np.empty((0,len(config.columns) * config.frames_counts * 5))
#         np_indicator_array = np.array([]) 
#         for exercise_combination in tqdm.tqdm(combinations): 
            
#             if exercise_combination[0].patientgroup in ['2', '3']:
#                 # Creating 5 empty array's 
#                 data_array = [np.array([]) for _ in range(len(exercise_combination))]

#                 for exercise_id in range(len(exercise_combination)):
#                     for exercise_frame in exercise_combination[exercise_id].np_frames:
#                         # Losse oefening [30]
#                         exercise_flat = exercise_frame.reshape(1, len(config.columns) * config.frames_counts)
#                         data_array[exercise_id] = np.append(data_array[exercise_id], exercise_flat[0])

#                 for data in data_array:
#                     np_combination_array = np.vstack ([np_combination_array, data])
#                     np_indicator_array = np.append(np_indicator_array, exercise_combination[0].patientgroup)
#             else:
#                 data = np.array([]) 
#                 for exercise in exercise_combination: 
#                     exercise_flat = exercise.np_data.reshape(1, len(config.columns) * config.frames_counts)
#                     data = np.append(data, exercise_flat[0])

#                 np_combination_array = np.vstack ([np_combination_array, data])
#                 np_indicator_array = np.append(np_indicator_array, exercise_combination[0].patientgroup)        

#         return np_combination_array, np_indicator_array


#     def generate_data(combinations):
#         np_combination_array = np.empty((0,len(config.columns) * config.frames_counts * config.exercise_count))
#         np_indicator_array = np.array([]) 
#         for exercise_combination in tqdm.tqdm(combinations): 
#             data = np.array([]) 
#             for exercise in exercise_combination:
#                 # Getting 5 frames from exercise
#                 exercise_flat = exercise.np_data.reshape(1, len(config.columns) * config.frames_counts)
#                 data = np.append(data, exercise_flat[0])

#             np_combination_array = np.vstack ([np_combination_array, data])
#             np_indicator_array = np.append(np_indicator_array, exercise_combination[0].patientgroup)

#         return np_combination_array, np_indicator_array




#     # print('np_combination_test, np_indicator_test: ', np_combination_test.shape, np_indicator_test.shape)
#     # print('np_combination_train, np_indicator_train: ', np_combination_train.shape, np_indicator_train.shape
