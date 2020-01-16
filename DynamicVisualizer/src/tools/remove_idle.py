import numpy as np
from config import config

class RemoveIdle():
    
    columns =  "humerus_r_y_plane", "humerus_r_z_ele", "humerus_r_y_ax"

    configs = { 
            'AB' : ('humerus_r_z_ele', 0.1),
            'AF' : ('humerus_r_y_ax', 0.1),
            'EL' : ('humerus_r_z_ele', 0.1),
            'RF' : ('humerus_r_z_ele', 0.1),
            'EH' : ('humerus_r_z_ele', 0.1),
        }

    def __init__(self,exercise):


        self.exercise = exercise
        self.bone, self.variatie = RemoveIdle.configs[self.exercise.exercisegroup]
        self.exercise_small = self.exercise.df[self.bone]
        self.exercise_split = np.array_split(self.exercise_small, config.remove_idle_split_count)

        self.exercise_small_diff = self.exercise_small.diff()
        self.data_head = self.exercise_split[0].diff()
        self.data_tail = self.exercise_split[-1].diff()

        self.begin = self.calculate_start() 
        self.the_end = self.calculate_end() 

        if self.begin < self.the_end:
            df_range = list(range(self.begin, self.the_end)) 
            self.df = self.exercise.df.iloc[df_range].copy() 
            
        else:
            self.df = self.exercise.df
            print('Error finding start or end')
    
    def calculate_start(self):
        self.start = self.exercise_small_diff > self.data_head.mean() +  float(self.variatie) * float(self.data_tail.mean())

        startindex = 0
        
        # 0 - 50 -> False 
        for a in range(0, self.exercise_small.shape[0]): 
            if self.start.iloc[a]:
                startindex = a 
                return startindex
        return 0 


    def calculate_end(self):
        self.end = self.data_tail > self.data_tail.mean() + float(self.variatie) * float(self.data_tail.mean())

        eindindex = self.exercise_small.shape[0]

        for a in reversed(range(0, self.end.shape[0])):
            exercise_length = self.exercise_small.shape[0]
            if self.end.iloc[a] == False:
                eindindex = exercise_length -  (self.end.shape[0] - a )
                return eindindex
        return exercise_length 
        