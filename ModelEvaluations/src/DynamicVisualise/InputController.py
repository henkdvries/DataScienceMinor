import sys
from multiprocessing import freeze_support
from tabulate import tabulate 
from patient.patientgroup import PatientGroup
from config import config 
import numpy as np
import matplotlib.pyplot as plt
from DynamicVisualise.DynamicVis import DynamicVisualiser
curpatgroup = 1
curpatindex = 0
patamount = 3
patient_groups = [
    PatientGroup(config.basepath.format(groupid=1)),
    PatientGroup(config.basepath.format(groupid=2)),
    PatientGroup(config.basepath.format(groupid=3)),
    PatientGroup(config.basepath.format(groupid=4)),
]


d = DynamicVisualiser(patient_groups[curpatgroup].patients[curpatindex:curpatindex+patamount],patamount)

def press(event):
    print('press', event.key)
    sys.stdout.flush()
    if event.key == 'j':
        return 0
    elif event.key == 'n':
        return 0
    elif event.key == 'up':
        return 0
    elif event.key == 'down':
        return 0
    elif event.key == 'right':
        d.update_tables(patient_groups[curpatgroup].patients[curpatindex+patamount+1], event.key)
        return 0
    elif event.key == 'left':
        return 0
    elif event.key == 'enter':
        return 0
    elif event.key == '1':
        curpatgroup = 1
    elif event.key == '2':
        curpatgroup = 2
    elif event.key == '3':
        curpatgroup = 3
    elif event.key == '4':
        curpatgroup = 4

        




fig1, ax2 = d.create_tables()

fig1.canvas.mpl_connect('key_press_event', press)
fig, ax = plt.subplots()

fig.canvas.mpl_connect('key_press_event', press)

ax.plot(np.random.rand(12), np.random.rand(12), 'go')
xl = ax.set_xlabel('easy come, easy go')
ax.set_title('Press a key')
plt.show()