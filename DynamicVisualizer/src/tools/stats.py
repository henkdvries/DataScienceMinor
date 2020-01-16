import itertools
import tabulate
from config import config

def print_group_stats(patient_groups):
    count = 0 
    table_data = []
    for patientgroup in patient_groups:
        for patient in patientgroup: 
            patient_data = {}
            for exercisegroup in config.exercisegroups: 
                patient_data[exercisegroup] = [] 
                for exercise in patient:
                    if exercise.exercisegroup == exercisegroup: 
                        patient_data[exercisegroup].append(exercise)
            if len(patient.exercises) > 0:
                print(patient.id)
                print(patient.path)
                patient_nr = int(patient.exercises[0].patientid)
                patientgroup = patient.exercises[0].patientgroup
                patient_groups = [value for key, value in patient_data.items()]
                resultaten = list(itertools.product(*patient_groups))
                count = count + len(resultaten)
                table_data.append([patientgroup, patient_nr,
                                    len(patient_data['AF']), len(patient_data['EL']), len(patient_data['AB']),
                                    len(patient_data['RF']), len(patient_data['EH']), len(resultaten),
                                    patient_nr in config.test_patients[patientgroup]])

    print(tabulate.tabulate(table_data, headers=[
                'catagorie', 'patientnummer', 'AF', 'EL', 'AB',
                'RF', 'EH', 'combinations', 'test person']))
                
    # 3437
    # 1856

    print(count) 