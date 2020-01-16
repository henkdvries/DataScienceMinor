
from config import config 
import numpy as np 
import matplotlib.pyplot as plt


class Removeidle:

    exercise_bone = { 
            'AB' : ('humerus_r_y_plane', 1.5),
            'AF' : ('humerus_r_y_plane', 1.5),
            'EL' : ('humerus_r_y_plane', 1.5),
            'RF' : ('humerus_r_y_plane', 1.5),
            'EH' : ('humerus_r_y_plane', 1.5),
        }

    def moving_average(self, a, n=3) :
        ret = np.cumsum(a, dtype=float)
        ret[n:] = ret[n:] - ret[:-n]
        return ret[n - 1:] / n

    def __init__(self, exercise):
        self.exercise = exercise 
        self.bone, self.variatie = Removeidle.exercise_bone[self.exercise.exercisegroup]

        self.np_data = self.exercise.df[self.bone].to_numpy()
        self.boneploty = self.exercise.df["humerus_r_y_plane"]
        self.boneplotx = self.exercise.df["humerus_r_y_ax"]
        self.boneplotz = self.exercise.df["humerus_r_z_ele"]


        self.difference = np.diff(self.moving_average(self.np_data))
        difference_split = np.array_split(self.difference, 6)
        self.difference_start = difference_split[0]
        self.difference_end = difference_split[-1]
        self.lenght = len(self.np_data)
 
        end = self.end() 
        start = self.start() 

        if start < end:
            df_range = list(range(start, end)) 
            self.df = self.exercise.df.iloc[df_range].copy() 
        else:
            self.df = self.exercise.df  

    def end(self):
        self.mean_end = np.mean(self.difference_end)
        variatie = self.variatie
        found = False 

        while not found: 
            if self.mean_end < 0: 
                mean_end_min = self.mean_end - (self.mean_end * -variatie)
                mean_end_max = self.mean_end + (self.mean_end * -variatie) 
            else:
                mean_end_min = self.mean_end - (self.mean_end * variatie)
                mean_end_max = self.mean_end + (self.mean_end * variatie)

            lijst = [] 
            
            reversed_list = np.flip(self.difference_end)

            for index, value in enumerate(reversed_list): 
                index = self.lenght - index - 1
                if reversed_list[0] > mean_end_max:
                    if value < mean_end_min: 
                        lijst.append(index)
                        # plt.plot(index - 2, value, marker='o', markersize=3, color="red")
                elif reversed_list[0] < mean_end_min:
                    if value > mean_end_max: 
                        lijst.append(index)
                        # plt.plot(index - 2, value, marker='o', markersize=3, color="red")
                else:  
                    if value > mean_end_max or value < mean_end_min:
                        lijst.append(index) 
                        # plt.plot(index - 2, value, marker='o', markersize=3, color="red")
            if lijst: 
                if len(lijst) > (len(self.difference_end)  * 0.5):
                    variatie = variatie * 1.3 
                else:   
                    found = True 
            else:
                variatie = variatie * 0.6   
        return lijst[0]


    def start(self):
        self.mean_start = np.mean(self.difference_start)
        
        variatie = self.variatie

        found = False 
        while not found: 
            if self.mean_start < 0: 
                mean_start_min = self.mean_start - (self.mean_start * -variatie)
                mean_start_max = self.mean_start + (self.mean_start * -variatie) 
            else:
                mean_start_min = self.mean_start - (self.mean_start * variatie)
                mean_start_max = self.mean_start + (self.mean_start * variatie)

            lijst = []
            for index, value in enumerate(self.difference_start): 
                if self.difference_start[0] > mean_start_max:
                    if value < mean_start_min: 
                        lijst.append(index)
                        # plt.plot(index, value, marker='o', markersize=3, color="red")
                elif self.difference_start[0] < mean_start_min:
                    if value > mean_start_max: 
                        lijst.append(index)
                        # plt.plot(index, value, marker='o', markersize=3, color="red")
                else:  
                    if value > mean_start_max or value < mean_start_min:
                        lijst.append(index) 
                        # plt.plot(index, value, marker='o', markersize=3, color="red")
            if lijst: 
                if len(lijst) > (len(self.difference_start)  * 0.5):
                        variatie = variatie * 1.3 
                else:   
                    found = True 
            else:
                variatie = variatie * 0.6  
        return lijst[0]

     
      
# plt.plot(self.difference) 
# plt.plot(self.np_data)
# plt.axvline(x=lijst[0], color='r', linestyle='-')
# plt.axhline(y=self.mean_end, color='r', linestyle='-')
# plt.axhline(y=mean_end_min, color='g', linestyle='-')
# plt.axhline(y=mean_end_max, color='yellow', linestyle='-')
# plt.plot(self.boneploty,label='y' )
# plt.plot(self.boneplotx,label='x' )
# plt.plot(self.boneplotz,label='z' )
# plt.axvline(x=(self.lenght - len(self.difference_end)), color='b', linestyle='-')
# plt.title('{bone} {group} {count}/{framecount}'.format(framecount=len(self.difference_start), count=len(lijst), bone=self.bone, group=self.exercise.exercisegroup))
# plt.axhline(y=self.mean_end, color='b', linestyle='-')
# plt.legend()
# plt.show()