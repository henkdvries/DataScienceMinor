import tqdm
import itertools
import numpy as np
import tabulate

from patient.patientgroup import PatientGroup

from config import config

import matplotlib.pyplot as plt

# importing 4 patient groups to import data
patient_groups = [
    PatientGroup(config.basepath.format(groupid=1)),
    PatientGroup(config.basepath.format(groupid=2)),
    PatientGroup(config.basepath.format(groupid=3)),
    PatientGroup(config.basepath.format(groupid=4))
]

# for now ... just look at the right humerus
xas = 'humerus_r_z_ele'
yas = 'humerus_r_y_plane'
zas = 'humerus_r_y_ax'

# to visualize just taken 1 exersice
exercise = patient_groups[0].patients[0].exercises[2]

# As the humerus has 3 angles to describe the rotation,
# I need two matices to capture the 'space' in wich the humerus
# moves. (matrix = 2D list)
table = np.zeros(shape=(36, 36))
tableb = np.zeros(shape=(36, 36))

# get the culumns out of the dataframe
list1 = exercise.df[xas].values
list2 = exercise.df[yas].values
list3 = exercise.df[zas].values

# loop through all datapoints of the exerce
# Every 'datapoint' has 3 values. See 'xas'
# 'yas' ans 'zas' definition, above.

# Every datapioint will add '1' to both table and tableb
# indicating that the this point in space was reached.
# To normalize this we are going to correct for the number
# os samples in the exercise, so we're not adding 1, but,
# 1/'number of samples'.

index = 0
increment = 1.0 / list1.size
for sample1 in list1:
    sample2 = list2[index]
    sample3 = list3[index]
    index = index+1

    # round every value down to a value between 0-36
    # To make the plot nicer, and to center the moves in the
    # plot, 180 degrees is added to every value.
    # (So, 0 degrees will shit to 180 degrees)
    nr1 = int(( (sample1+180) % 360) / 10)
    nr2 = int(( (sample2+180) % 360) / 10)
    nr3 = int(( (sample3+180) % 360) / 10)

    # Fill the datapoint to the resultmetrices
    table[nr2][nr1] = table[nr2][nr1] + increment
    tableb[nr3][nr1] = tableb[nr3][nr1] + increment
    
# plot the matrices with the result
plt.matshow(table, cmap=plt.get_cmap('jet'))
plt.xlabel(xas)
plt.ylabel(yas)

plt.matshow(tableb, cmap=plt.get_cmap('jet'))
plt.xlabel(xas)
plt.ylabel(zas)
plt.show()
