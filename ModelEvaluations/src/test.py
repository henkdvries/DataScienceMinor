import sys
from multiprocessing import freeze_support
from tabulate import tabulate 
from patient.patientgroup import PatientGroup
from config import config 
import numpy as np
import matplotlib.pyplot as plt
from DynamicVisualise.DynamicVis import DynamicVisualiser
import pprint as pp


patient_groups = [
    #PatientGroup(config.basepath.format(groupid=1)),
    #PatientGroup(config.basepath.format(groupid=2)),
    #PatientGroup(config.basepath.format(groupid=3)),
   # PatientGroup(config.basepath.format(groupid=4)),
]
bones = (("clavicula_r_y_pro", "clavicula_r_z_ele", "clavicula_r_x_ax"),
        ("scapula_r_y_pro", "scapula_r_z_lat", "scapula_r_x_tilt"),
        ("humerus_r_y_plane", "humerus_r_z_ele", "humerus_r_y_ax"))

   

patientgroup = [
    PatientGroup(config.basepath.format(groupid=1)),
    PatientGroup(config.basepath.format(groupid=2)),
    PatientGroup(config.basepath.format(groupid=3))
    ]
groupdict = {}
for index, groups in enumerate(patientgroup):
    groupdict[index] = [{'exercises':patient.exercises, 
                'groupid':groups.id,
                'id':patient.id } 
                for patient in groups.patients]
    
#
# {
#   0: {
#       
#   }
# }
#
#


for key in groupdict.keys():
    for patient in groupdict[key]:
        patient['groups'] = {}
        for exercise in patient['exercises']:
            if exercise.exercisegroup not in patient['groups']:
                patient['groups'][exercise.exercisegroup] = []
            patient['groups'][exercise.exercisegroup].append(exercise)

d = DynamicVisualiser(groupdict)
d.create_tables()
d.update_tables() 

plt.show()

