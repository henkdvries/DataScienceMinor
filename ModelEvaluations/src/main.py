from multiprocessing import freeze_support
from tabulate import tabulate 
from patient.patientgroup import PatientGroup
from config import config 
from tools.visualis import Visualize
from DynamicVisualise.InputController import InputController
from matplotlib.backend_bases import key_press_handler

#config.exercisegroups = ['AF', ]
config.raw_visualization_enabled = False
config.raw_visualization_autoplay = False

patient_groups = [
    PatientGroup(config.basepath.format(groupid=1)),
    PatientGroup(config.basepath.format(groupid=2)),
    PatientGroup(config.basepath.format(groupid=3)),
    PatientGroup(config.basepath.format(groupid=4)),
]

# for patientlist in patient_groups:
#     for patient in patientlist:
    
#         henk = Visualize(data =patient, exercises= ['AF', 'EL', 'AB'], bones = ("clavicula_r_y_pro", "clavicula_r_z_ele", "clavicula_r_x_ax",
#                     "scapula_r_y_pro", "scapula_r_z_lat", "scapula_r_x_tilt",
#                     "humerus_r_y_plane", "humerus_r_z_ele", "humerus_r_y_ax"
#                     ))
#         henk.visualise()


d = InputController()