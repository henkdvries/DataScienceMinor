import matplotlib.pyplot as plt
from patient.patient import Patient
from patient.exercise import Exercise
import numpy as np
import random
import json
import traceback
class DynamicVisualiser:
   
    NPATIENTS = 3
    BONES = [["clavicula_r_y_pro", "clavicula_r_z_ele", "clavicula_r_x_ax"],
            ["scapula_r_y_pro", "scapula_r_z_lat", "scapula_r_x_tilt"],
            ["humerus_r_y_plane", "humerus_r_z_ele", "humerus_r_y_ax"]]
    EXERCISE = ['AF', 'EL', 'AB', 'RF', 'EH']
    
    def __init__(self, data, bones = None):
        # list of 3 patients
        self.patients = data 
        self.figure = None
        self.axis = None
        self.bones = bones
        self.patient_index = 0
        self.exercise_index = 0
        self.curpatgroup = 0 
        self.colors = plt.cm.jet(np.linspace(0, 1, len(self.patients[self.curpatgroup])))
        np.random.shuffle(self.colors)
        self.jsondata = {}
        self.jsondata['patients'] = {}
        # TODO: LOSSE OEFENINGEN VAN PATIENT IN LIJST ZETTEN, 
        # WAARDOOR ER DOOR OEFENINGEN WORDT GELOPEN, NIET PATIENTEN

        
    def create_tables(self):
        plt.ion()
        self.figure, self.axis = plt.subplots(len(DynamicVisualiser.BONES[0]), DynamicVisualiser.NPATIENTS, sharex= True, sharey= True)
        self.figure.canvas.mpl_connect('key_press_event', self.press)

        self.plots = []
        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)
        

        for row in self.axis:
            for axis in row:
                self.plots.append(axis.plot(t, s))    
        # self.figure.canvas.draw()
        plt.show(block=True)
    
    def update_tables(self, outofbounds = None): 
        line_styles = ['-', '--', '-.', ':']
        print('update tables')
        if outofbounds is None:
            for bone_index, column in enumerate(self.axis):
                for index, axis in enumerate(column):
                    axis.clear()
                    patientindex = index + self.patient_index
                    patient = self.patients[self.curpatgroup][patientindex]
                    exercises = patient['groups'][DynamicVisualiser.EXERCISE[self.exercise_index]]
                    axis.set_title("{group}-{id}-{ex}".format(group=patient['groupid'], id=patient['id'], ex=DynamicVisualiser.EXERCISE[self.exercise_index]))
                    axis.set_xlabel = 'Frames'
                    axis.set_ylabel = DynamicVisualiser.BONES[bone_index]
                    for exercise_index ,exercise in enumerate(exercises):
                        axis.plot(exercises[exercise_index].dataframe[DynamicVisualiser.BONES[bone_index]], c=self.colors[patientindex], linestyle=line_styles[exercise_index])
                    # print(exercises[bone_index], bone_index)
        elif outofbounds == 'upper':
            for bone_index, column in enumerate(self.axis):
                for index, axis in enumerate(column):
                    axis.clear()
                    if(index + self.patient_index  < len(self.patients)):
                        patientindex = index + self.patient_index
                    else:
                        patientindex = index
                        
                    patient = self.patients[self.curpatgroup][patientindex]
                    exercises = patient['groups'][DynamicVisualiser.EXERCISE[self.exercise_index]]
                    axis.set_title("{group}-{id}-{ex}".format(group=patient['groupid'], id=patient['id'], ex=DynamicVisualiser.EXERCISE[self.exercise_index]))
                    axis.set_xlabel = 'Frames'
                    for exercise_index ,exercise in enumerate(exercises):
                        axis.plot(exercises[exercise_index].dataframe[DynamicVisualiser.BONES[bone_index]], c=self.colors[patientindex], linestyle= line_styles[exercise_index])
                    
        elif outofbounds == 'lower':
            for bone_index, column in enumerate(self.axis):
                for index, axis in enumerate(column):
                    axis.clear()
                    patientindex = index + self.patient_index
                    patient = self.patients[self.curpatgroup][patientindex]
                    exercises = patient['groups'][DynamicVisualiser.EXERCISE[self.exercise_index]]
                    axis.set_title("{group}-{id}-{ex}".format(group=patient['groupid'], id=patient['id'], ex=DynamicVisualiser.EXERCISE[self.exercise_index]))
                    axis.set_xlabel = 'Frames'
                    axis.set_ylabel = DynamicVisualiser.BONES[bone_index]
                    for exercise_index ,exercise in enumerate(exercises):
                        axis.plot(exercises[exercise_index].dataframe[DynamicVisualiser.BONES[bone_index]], c=self.colors[patientindex], linestyle= line_styles[exercise_index])
   
    def press(self, event):
        print('press', event.key)
        
        if event.key == 'u':
            self.update_tables() 
        elif event.key == 'right':
            # TODO: Check index out of range (reset at beginning)
            print(self.patient_index, len(self.patients[self.curpatgroup]))
            if self.patient_index + 1 > len(self.patients[self.curpatgroup]) - DynamicVisualiser.NPATIENTS:
                
                if(self.patient_index == len(self.patients[self.curpatgroup])-1):
                    self.patient_index = 0
                    print("upper bound")
                else:
                    self.patient_index += 1
                self.update_tables('upper')
            else:
                self.patient_index = self.patient_index + 1
                self.update_tables()
        elif event.key == 'left':
            # TODO: Check index out of range (reset at beginning)
            print(self.patient_index, len(self.patients[self.curpatgroup]))
            if self.patient_index - 1 < 0 :
                self.patient_index = self.patient_index -1 
                self.update_tables('lower')
            else:
                self.patient_index = self.patient_index -1
                self.update_tables()
                
        elif event.key == 'j':
            try:
                if DynamicVisualiser.EXERCISE[self.exercise_index] not in self.jsondata['patients'][str(self.patient_index)]['exercise']:
                    self.jsondata['patients'][str(self.patient_index)]['exercise'].append(DynamicVisualiser.EXERCISE[self.exercise_index])
                    self.jsondata['patients'][str(self.patient_index)]['patientgroup'] = self.curpatgroup +1
                
                    
            except Exception:
                traceback.print_exc()
                print('try 1')
                try:
                    self.jsondata['patients'][str(self.patient_index)] = { 'exercise': [DynamicVisualiser.EXERCISE[self.exercise_index]]}
                    self.jsondata['patients'][str(self.patient_index)]['patientgroup'] = self.curpatgroup +1 
                except Exception:
                    traceback.print_exc()
                    print('try 2')
            print(self.jsondata['patients'][str(self.patient_index)])        
            
           
        elif event.key == 'n':
            return 0
        elif event.key == 'up':
            if(len(self.EXERCISE)-1 > self.exercise_index):
                self.exercise_index += 1
                self.update_tables()
        elif event.key == 'down':
            if(self.exercise_index > 0):
                self.exercise_index -= 1
                self.update_tables()
        elif event.key == 'enter':
            self.jsonwriter()
        elif event.key == '1':
            self.curpatgroup = 0
            self.patient_index = 0
            self.colors = plt.cm.jet(np.linspace(0, 1, len(self.patients[self.curpatgroup])))
            np.random.shuffle(self.colors)
            self.update_tables
        elif event.key == '2':
            self.curpatgroup = 1
            self.patient_index = 0
            self.colors = plt.cm.jet(np.linspace(0, 1, len(self.patients[self.curpatgroup])))
            np.random.shuffle(self.colors)
            self.update_tables
        elif event.key == '3':
            self.curpatgroup = 2
            self.patient_index = 0
            self.colors = plt.cm.jet(np.linspace(0, 1, len(self.patients[self.curpatgroup])))
            np.random.shuffle(self.colors)
            self.update_tables
        elif event.key == '4':
            return 0


    def jsonwriter(self):
        with open('wrongfiles.json', 'w') as output:
            json.dump(self.jsondata, output, indent= 4)