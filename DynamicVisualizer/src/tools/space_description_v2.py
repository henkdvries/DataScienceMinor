import tqdm
import itertools
import numpy as np
import pandas as pd
import tabulate
from patient.patientgroup import PatientGroup
from config import config
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from tools.visualis import Visualis

from sklearn.cluster import KMeans


# importing 4 patient groups to import data
patient_groups = [
    PatientGroup(config.basepath.format(groupid=1)),
    #PatientGroup(config.basepath.format(groupid=2)),
    #PatientGroup(config.basepath.format(groupid=3)),
    #PatientGroup(config.basepath.format(groupid=4))
]

nbbins = 360
binsize = 360 / nbbins


# Define a 3d space ontaied by 3 axes (as1 as2 as3).
# Calculate what part of this space is occupied during the given
# excercise.
def def_space(exercise, as1, as2, as3):


    # I need two matices to capture the 'space' in wich the humerus
    # moves. (matrix = 2D list)
    #tablea = np.zeros(shape=(nbbins, nbbins))
    #tableb = np.zeros(shape=(nbbins, nbbins))

    # As the humerus has 3 angles to describe the rotation,
    # i make a 3d array.
    tableall = np.zeros(shape=(nbbins, nbbins, nbbins))

    # get the culumns out of the dataframe
    list1 = exercise.df[as1].values
    list2 = exercise.df[as2].values
    list3 = exercise.df[as3].values

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
        # (So, 0 degrees will shift to 180 degrees)
        nr1 = int(((sample1 + 180) % 360) / binsize)
        nr2 = int(((sample2 + 180) % 360) / binsize)
        nr3 = int(((sample3 + 180) % 360) / binsize)

        # Fill the datapoint to the resultmetrices
        #tablea[nr1][nr2] = tablea[nr1][nr2] + increment
        #tableb[nr1][nr3] = tableb[nr1][nr3] + increment

        tableall[nr1][nr2][nr3] = 1

    # plot the matrices with the result
    '''
    plt.figure()

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')

    plt.suptitle(exercise.exercisestype)
    plt.subplot(1, 2, 1)
    plt.matshow(tablea, fignum=0, cmap=plt.get_cmap('jet'))
    plt.xlabel(as2)
    plt.ylabel(as1)

    plt.subplot(1, 2, 2)
    plt.matshow(tableb, fignum=0, cmap=plt.get_cmap('jet'))
    plt.xlabel(as3)
    plt.ylabel(as1)
    plt.show()
    '''
    # x, y, z = tableall.nonzero()

    # fig = plt.figure()
    # plt.suptitle(exercise.exercisestype)
    # ax = fig.add_subplot(111, projection='3d')
    # ax.set_xlim3d([0, 360])
    # ax.set_ylim3d([0, 360])
    # ax.set_zlim3d([0, 360])
    # ax.set_xlabel(as1)
    # ax.set_ylabel(as2)
    # ax.set_zlabel(as3)

    # ax.scatter(x, y, z, s=10, zdir='z', c='red')
    #plt.show()


    

    return tableall # tablea, tableb


# for now ... just look at the right humerus
as_a = 'humerus_r_z_ele'
as_b = 'humerus_r_y_plane'
as_c = 'humerus_r_y_ax'

tab = np.zeros(shape=(nbbins, nbbins, nbbins))
#tabb = np.zeros(shape=(nbbins, nbbins))

'''
exercise = patient_groups[0].patients[1].exercises[0]
t, tb = def_space(exercise, as_a, as_b, as_c)
tab = tab + t
tabb = tabb + tb
'''
df_list = []
for group in patient_groups:
    for patient in group.patients:
        if int(patient.exercises[0].patientid) < 4:
            tab = np.zeros(shape=(nbbins, nbbins, nbbins))
            t = def_space(patient.exercises[0], as_a, as_b, as_c)
            #t, tb = def_space(exercise, as_a, as_b, as_c)
            #tab = tab + t
            #tabb = tabb + tb
            tab = np.logical_or(tab, t)
            x, y, z = tab.nonzero()
            d = {'x': x, 'y': y, 'z': z}
            df_list.append(pd.DataFrame(data = d))
            
            print(df_list[0])





# fig = plt.figure()
# plt.suptitle("total occupied space patient")
# ax = fig.add_subplot(111, projection='3d')
# ax.set_xlim3d([0, 360])
# ax.set_ylim3d([0, 360])
# ax.set_zlim3d([0, 360])
# ax.set_xlabel(as_a)
# ax.set_ylabel(as_b)
# ax.set_zlabel(as_c)

# ax.scatter(x, y, z, s=10, zdir='z', c='red')
# plt.show()

'''
plt.figure()
plt.suptitle("total occupied space patient 1")
plt.subplot(1, 2, 1)
plt.matshow(tab, fignum=0, cmap=plt.get_cmap('jet'))
plt.xlabel(as_b)
plt.ylabel(as_a)

plt.subplot(1, 2, 2)
plt.matshow(tabb, fignum=0, cmap=plt.get_cmap('jet'))
plt.xlabel(as_c)
plt.ylabel(as_a)
plt.show()
'''
# estimator = [('k_means_3D_8', KMeans(n_clusters=8)),
#               ('k_means_3D_3', KMeans(n_clusters=3))]

# fignum = 1
# titles = ['8 cluster', '3 cluster']
# for name, est in estimator:
#     fig = plt.figure(fignum)
#     ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
#     est.fit(y.reshape(-1, 1))
#     labels = est.labels_

#     ax.scatter(x,y,z, c=labels.astype(np.float), edgecolor = 'k')

#     ax.w_xaxis.set_ticklabels([])
#     ax.w_yaxis.set_ticklabels([])
#     ax.w_zaxis.set_ticklabels([])
#     ax.set_xlabel('Petal width')
#     ax.set_ylabel('Sepal length')
#     ax.set_zlabel('Petal length')
#     ax.set_title(titles[fignum - 1])
#     ax.dist = 12
#     fignum = fignum + 1
# plt.show()


v = Visualis(patient_groups)
v.visualise_k_means(df_list[0])