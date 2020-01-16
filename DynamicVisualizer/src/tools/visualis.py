import itertools
import random
import matplotlib.pyplot as plt 
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import matplotlib as mpl
import numpy as np 
import pandas as pd
import pprint


from sklearn.cluster import KMeans
from mpl_toolkits.mplot3d import Axes3D

from tools.remove_idle import RemoveIdle 

from config import config


class Visualize: 


    def __init__(self, data, catagory = None, patients = None, exercises = None, bones = None):
        self.left = True 
        self.right = True 
        self.lines = False 

        self.data = data
        self.catagory = catagory 
        self.patients = patients 
        self.exercises = exercises 

        self.bones = bones 
        self.unique_patients = []

        self.filtered_data = [] 
        self.filter_data() 

        self.generate_metadata()

        self.colors = []
        self.l_styles = ['-','--','-.',':']


    def visualise_exercise(self, exercise, column):
        # Unpacking exercise 
        # Based on the row index from self.bones 

        for index, bone in enumerate(self.bones):
            # TODO: check for multiple rows

            color = self.unique_patients.index(self.get_unique_patientnr(exercise.patientgroup, exercise.patientid))
            linestyle = self.l_styles[int(exercise.patientgroup)-1]
            
            # Extract the data 
            df = exercise.dataframe[[bone]].reset_index(drop=True)
            if len(self.bones) is 1:
                try:
                    self.axs[column].plot(df, c=self.colors[color], linestyle=linestyle)
                except TypeError:
                    self.axs.plot(df, c=self.colors[color], linestyle=linestyle)
            try:
                try:
                    self.axs[index].plot(df, c=self.colors[color], linestyle=linestyle)
                except:
                    self.axs[column].plot(df, c=self.colors[color], linestyle=linestyle)
            except:
                try:
                    self.axs[index,column].plot(df, c=self.colors[color], linestyle=linestyle)
                except:
                    self.axs.plot(df, c=self.colors[color], linestyle=linestyle)
            # plot the data 
            

        # Row is based on data inside of the exercise 

    def visualize_idle(self, exercise, column):

        for index, bone in enumerate(self.bones):
            df = exercise.df[[bone]].reset_index(drop=True)
            
            row = self.unique_patients.index(self.get_unique_patientnr(exercise.patientgroup, exercise.patientid))

            colorshift = 0.5

            startcolor = np.array([1.0,0.0,0.0,1.0])
            endcolor = np.array([0.0,0.0,1.0,1.0])
            color = self.colors[row]
            
            if int(exercise.exercisestype[2]) % 2 is 0:
                startcolor = startcolor * colorshift
                endcolor = startcolor * colorshift
                color = color * colorshift


            linestyle = self.l_styles[int(exercise.patientgroup)-1]
            

            start= exercise.begin
            end = exercise.end
            
            if len(self.unique_patients) is 1:
                try:
                    self.axs[column].axvline(x=start, c=startcolor)
                    self.axs[column].axvline(x=end, c=endcolor)
                    self.axs[column].plot(df, c=color, linestyle=linestyle)
                except TypeError:
                    self.axs.axvline(x=start, c=startcolor)
                    self.axs.axvline(x=end, c=endcolor)
                    self.axs.plot(df, c=color, linestyle=linestyle)
            else:
                try:
                    self.axs[row,column].axvline(x=start, c=startcolor)
                    self.axs[row,column].axvline(x=end, c=endcolor)
                    self.axs[row,column].plot(df, c=color, linestyle=linestyle)
                except IndexError:
                    self.axs[row].axvline(x=start, c=startcolor)
                    self.axs[row].axvline(x=end, c=endcolor)
                    self.axs[row].plot(df, c=color, linestyle=linestyle)
                except TypeError:
                    self.axs.axvline(x=start, c=startcolor)
                    self.axs.axvline(x=end, c=endcolor)
                    self.axs.plot(df, c=color, linestyle=linestyle)


    def visualise(self, mode = None): 
        # TODO: Setting plot title 

        if mode == 'idle':
            self.fig, self.axs = plt.subplots(
                len(self.unique_patients),
                len(self.exercises))
            self.set_title(self.fig, 'this a visulization')
            print('Created plot with {cols} cols and {rows} rows'.format(cols=len(self.exercises), rows=len(self.unique_patients)))
            
            self.generate_colors_patients()

            # Looping through filtered exercises 
            for exercise in self.filtered_data:
                column_index = self.exercises.index(exercise.exercisegroup)
                # self.visualise_exercise(exercise, column_index)
                self.visualize_idle(exercise, column_index)
            #setting labels vor legend
            self.set_label(self.axs, self.exercises, self.unique_patients)
            self.set_legend(self.fig, self.unique_patients, self.colors, self.l_styles)
            plt.show() 


        elif mode == 'exercise':
            self.fig, self.axs = plt.subplots(
                len(self.bones),
                len(self.exercises))
            self.set_title(self.fig, 'this a visulise')
            print('Created plot with {cols} cols and {rows} rows'.format(cols=len(self.exercises), rows=len(self.bones)))
            
            self.generate_colors_patients()

            # Looping through filtered exercises 
            for exercise in self.filtered_data:
                column_index = self.exercises.index(exercise.exercisegroup)
                self.visualise_exercise(exercise, column_index)


              #setting labels vor legend
            self.set_label(self.axs, self.exercises, self.bones)
            self.set_legend(self.fig, self.unique_patients, self.colors, self.l_styles)
            plt.show() 
        else:
            raise('mode needs to be set either to "idle" or "exercise"')
        



    def visualise_k_means(self, df):
        estimator = [('k_means_3D_8', KMeans(n_clusters=8)),
              ('k_means_3D_3', KMeans(n_clusters=3))]

        fignum = 1
        titles = ['8 cluster', '3 cluster']
        for name, est in estimator:
            fig = plt.figure(fignum)
            ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
            est.fit(y.reshape(-1, 1))
            labels = est.labels_

            ax.scatter(df[:,0],df[:,1],df[:,2], c=labels.astype(np.float))

            ax.w_xaxis.set_ticklabels([])
            ax.w_yaxis.set_ticklabels([])
            ax.w_zaxis.set_ticklabels([])
            ax.set_xlabel('Petal width')
            ax.set_ylabel('Sepal length')
            ax.set_zlabel('Petal length')
            ax.set_title(titles[fignum - 1])
            ax.dist = 12
            fignum = fignum + 1

        
        plt.show()



    def generate_metadata(self):
        categories = []
        exercies = []
        uniques = []
        if not self.bones:
            self.bones = config.columns
        #loop through all the exercises for the visualisation
        for exercise in self.filtered_data:
            #set patientgroups
            if not self.catagory:
                if int(exercise.patientgroup) not in categories:
                    categories.append(int(exercise.patientgroup))    
                
            #set exercises
            if not self.exercises:   
                if exercise.exercisegroup not in exercies:
                    exercies.append(exercise.exercisegroup)
                   
            #set unique patients
            if not self.patients:  
                # loop through all exercises to find unique patients
                unique = exercise.unique_patientnr
                if unique not in uniques:
                    uniques.append(unique)
        if not self.exercises:
            self.exercises = exercies 
        if not self.catagory:
            self.catagory = categories
        if self.patients:
            for c in self.catagory:
                for p in self.patients:
                    unique = self.get_unique_patientnr(c,p)
                    if unique not in uniques:
                        uniques.append(unique)
        
        self.unique_patients = uniques
        

    def filter_data(self):
        # Getting all exercises 
        for patientgroup in self.data: 
            for patient in patientgroup:
                for exercise in patient:
                    skip = False
                    # If catagory is not none, we want to filter 
 
                    if self.catagory:
                        if int(exercise.patientgroup) not in self.catagory:  
                            skip = True 

                    if self.patients and not skip: 
                        if int(exercise.patientid) not in self.patients: 
                            skip = True  

                    if self.exercises and not skip: 
                        if exercise.exercisegroup not in self.exercises: 
                            skip = True 

                    if not skip: 
                        self.filtered_data.append(exercise)
    
    def generate_colors_patients(self):
        #how many patients?
        
        #left and right separate?
        self.colors = plt.cm.jet(np.linspace(0,1,len(self.unique_patients)))

    def get_unique_patientnr(self, patientgroup, patientid):
        unique = str(patientgroup)+ ','+ str(patientid)
        return unique
    
    def set_title(self,fig, title = 'Plot '):
        fig.suptitle(title + ' of Patientgroups: ' + str(self.catagory) + 
                    ' containing ' + (str(len(self.patients)) + ' patients' if self.patients is not None else 'all patients'))

    def set_legend(self,fig, color_correl, colors, l_styles):
        labels = []
        handels = []
        for var in color_correl:
            labels.append(var)
        for c in colors:
            handels.append(mpatches.Patch(color = c))
        for i, l in enumerate(l_styles):
            labels.append('Cat ' + str(i+1))
            handels.append(mlines.Line2D((0,0), (1,1),linestyle=l, color = 'black'))
        if len(colors) < 46:
             fig.legend(handles=handels, labels=labels, loc="upper left")
        elif len(colors) > 46 and len(colors) < 93:
            fig.legend(handles=handels, labels=labels, ncol=2, loc="upper left")
        elif len(colors) > 93:
            fig.legend(handles=handels[:92], labels=labels[:92], ncol=2, loc="upper left")
            fig.legend(handles=handels[93:], labels=labels[93:], loc="upper rigtht")
        else:
            fig.legend(handles=handels[:92], labels=labels[:92], ncol=2, loc="upper left")
            fig.legend(handles=handels[93:], labels=labels[93:], ncol=2, loc="upper rigtht")

    def set_label(self,axs, cols, rows):
        try:
            for ax, col in zip(axs[0], cols):
                ax.set_title(col)
            for ax, row in zip(axs[:,0], rows):
                ax.set_ylabel(row, rotation=0, size='large')

        except TypeError:
            try:
                for ax, col in zip(axs, cols):
                    ax.set_title(col)
                for ax, row in zip(axs, rows):
                    ax.set_ylabel(row, rotation = 0, size = 'large')
            except:
                axs.set_title(cols[0])
                axs.set_ylabel(rows[0], rotation = 0, size = 'large')
        
            
        except:
            print("It's all fucked")
