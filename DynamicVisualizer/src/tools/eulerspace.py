
import numpy as np
import matplotlib.pyplot as plt

from config import config 



# Plot a 2d / 3d matrix. All axes are set to [0,nbbins]
# Parameters:
# mat : the matrix (correct size is NOT chacked)
# axes : a tuple with the axes names
# title : title of the figure
def plot2d3dmatrix(mat, axes, title="", color='red'):
    nbbins = config.binsize
    binsize = 360 / nbbins

    if len(axes) == 3:
        x, y, z = mat.nonzero()

        fig = plt.figure()
        plt.suptitle(title)
        ax = fig.add_subplot(111, projection='3d')

        # scale back to -180 to 180 degrees
        halfbin = nbbins/2
        ax.set_xlim3d([-180, 180])
        ax.set_ylim3d([-180, 180])
        ax.set_zlim3d([-180, 180])
        ax.set_xlabel(axes[0])
        ax.set_ylabel(axes[1])
        ax.set_zlabel(axes[2])
        ax.scatter((x-halfbin)*binsize,
                   (y-halfbin)*binsize,
                   (z-halfbin)*binsize, s=10, zdir='z', c='red')

        '''
        ax.set_xlim3d([0, nbbins])
        ax.set_ylim3d([0, nbbins])
        ax.set_zlim3d([0, nbbins])
        ax.set_xlabel(axes[0])
        ax.set_ylabel(axes[1])
        ax.set_zlabel(axes[2])

        ax.scatter(x, y, z, s=10, zdir='z', c='red')
        '''
        plt.show()

    if len(axes) == 2:
        plt.figure()

        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')

        plt.suptitle(title)
        plt.matshow(mat, fignum=0, cmap=plt.get_cmap('jet'))
        plt.xlabel(axes[1])
        plt.ylabel(axes[0])
        plt.show()
        #plt.draw()
        #plt.pause(0.001)


# Define a n-dimentional space contaied by the axes .
# Calculate what part of this space is occupied during the given
# excercise.
# The function depends on the following global vars: nbbins & binsize
# parameters:
#   exercise = excercise class
#   axes = tuple with the axes defining the space to calculate.
#          these are collums as defined in config.py
#   plot = plot the calculated space (2D / 3D only!)
#   count = if True,the returned array contains floats representing the
#           amount of samples found in that bin. If False, the returned array
#           contians just 0 and 1 values, depending if samples are found in
#           that bin.
# return: a n dimentional array representing the space used.
def def_space(exercise, axes, plot=False, count=True):
    nbbins = config.binsize
    binsize = 360 / nbbins

    # Define the dimensions of the result table based on the number
    # of axes.
    dimension = (nbbins,)*len(axes)
    # at this moment just make the resultarray one dimentional
    tableall = np.zeros(pow(nbbins, len(axes)))

    if len(axes) <= 0:
        return tableall

    # get the columns out of the dataframe of exercise
    list = []
    for elm in axes:
        list.append(exercise.dataframe[elm].to_numpy())

    # Every datapioint will add '1' to both table and tableb
    # indicating that the this point in space was reached.
    # To normalize this we are going to correct for the number
    # os samples in the exercise, so we're not adding 1, but,
    # 1/'number of samples'.
    increment = 1.0 / list[0].size

    for i in (range(list[0].size)):

        # Get all samples data from the exersice
        sample = []
        for dim in range(len(axes)):
            samplevalue = list[dim][i]

            # Round every value (range [0,360]) down to a int value based on
            # the binsize. To make the plot nicer, and to center the moves
            # in the plot, 180 degrees is added to every value.
            # (So, 0 degrees will shift to 180 degrees)
            nr = int(((samplevalue + 180) % 360) / binsize)
            sample.append(nr)

        # Calculate the index of the sample in the resultmatrix
        tableall_index = 0
        for nr in sample:
            tableall_index = (tableall_index*nbbins)+nr

        # Fill the datapoint to the resultmetrix
        if count:
            tableall[tableall_index] = tableall[tableall_index] + increment
        else:
            tableall[tableall_index] = 1

    # Now reshape the resultmatix to the correct dimentions
    tableall = np.reshape(tableall, dimension)

    # plot the matrices with the result if the dimention is 2 or 3
    if 0 < len(axes) <= 3:
        if plot:
            plot2d3dmatrix(tableall, axes, title=exercise.exercisestype)

    return tableall
