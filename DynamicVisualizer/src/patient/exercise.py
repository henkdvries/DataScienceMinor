import os
import pandas as pd
import math 
import numpy as np
from config import config
from tools.visualiseraw import VisualiseRaw 
# from tools.remove_idle import RemoveIdle
from tools.resample import resample_excercise

from tools.removeidle import Removeidle




class Exercise:
    sizes = []

    columns = {
        0: "thorax_r_x_ext", 1: "thorax_r_y_ax", 2: "thorax_r_z_lat",
        3: "clavicula_r_y_pro", 4: "clavicula_r_z_ele", 5: "clavicula_r_x_ax",
        6: "scapula_r_y_pro", 7: "scapula_r_z_lat", 8: "scapula_r_x_tilt",
        9: "humerus_r_y_plane", 10: "humerus_r_z_ele", 11: "humerus_r_y_ax",
        12: "ellebooghoek_r",
        15: "thorax_l_x_ext", 16: "thorax_l_y_ax", 17: "thorax_l_z_lat",
        18: "clavicula_l_y_pro", 19: "clavicula_l_z_ele", 20: "clavicula_l_x_ax",
        21: "scapula_l_y_pro", 22: "scapula_l_z_lat", 23: "scapula_l_x_tilt",
        24: "humerus_l_y_plane", 25: "humerus_l_z_ele", 26: "humerus_l_y_ax",
        27: "ellebooghoek_l"
    }

    def __init__(self, path: str):
        self.path = path
        self.raw_path = path.replace('.csv', '.txt', 1)

        # extracting path exercise type and type of exercise 
        exercisepath, self.exercisestype = os.path.split(self.path)          
        grouppath, self.patientid = os.path.split(exercisepath) 
        self.patientgroup = grouppath[-1]
        self.exercisegroup = self.exercisestype[:2]
        self.unique_patientnr = self.get_unique_patientnr(self.patientgroup, self.patientid)
        
        # Reading data; df should be read-only
        self.df = pd.read_csv(self.path, names=list(range(30)))
        self.df = self.df.rename(columns=Exercise.columns)
        
        # Doing something with the raw data - visualistation
        self.update_config() 
        # self.raw = VisualiseRaw(self.raw_path, self)

        if config.differentiation:
            self.filtered_signal = self.lowpassfilter(1/6, 1 / (2 * math.pi * 0.5)) 
            self.differentiation = self.differentiation(self.filtered_signal)

  
    def differentiation(self, y,  h=1):
        '''Compute the difference formula for f'(a) with step size h.
            Parameters
            ----------
            f : function
                Vectorized function of one variable
            a : number
                Compute derivative at x = a
            method : string
                Difference formula: 'forward', 'backward' or 'central'
            h : number
                Step size in difference formula
            '''
        differentiation = np.zeros((y.shape[0], 1))
        for i, value in enumerate(range(y.shape[0] - 1), 1):
            differentiation[i] = (y[i] - y[i-1]) / (1/6)

        return differentiation 

    # TODO: Implement function on all bones!! 
    def lowpassfilter(self, dt, RC):
        # RC: time constant - related to cut off freq
        # dt: time interval 
        x = self.df.to_numpy()[:,0]  
        y = np.zeros((self.df.shape[0], 1))
        yy = np.zeros((self.df.shape[0], 1))
        a = dt / (RC + dt)  
        y[0] = x[0] 
        
        for i, value in enumerate(range(x.shape[0] - 1), start=1):    
            y[i] = a * x[i] + (1-a) * y[i-1]
        
        return y 
         
    def update_config(self): 
        # If we want to remove idle
        if config.remove_idle:
            self.idle = Removeidle(self)
            self.end = self.idle.end()
            self.begin = self.idle.start()
            self.dataframe = self.idle.df
            #print('done removing idle and generating dataframes',self.dataframe.shape) 
        else: 
            self.dataframe = self.df.copy()
        if config.resample_exercise:
            # resample_excercise returns only the colums from config.columns
            self.dataframe = resample_excercise(self.dataframe, config.frames_counts)
        else:
            # Making a small dataframe of 5 rows by multipling the rows with the columns
            frames = self.get_frames()
            #print(frames, self.dataframe.head())
            self.dataframe = self.dataframe[config.columns].iloc[frames]

        if config.frame_generator:
            self.np_frames = [] 
            self.gen_frames()

        # Compute the numpy array of dataframe by using .to_numpy
        self.np_data = self.dataframe.to_numpy() 

    
    def df_regex(self, pattern):
        # Left          r"._l_."
        # Right         r"._r_."
        return self.dataframe.filter(regex=(pattern))

    def gen_frames(self):
        frames = self.get_frames()
        new_frame_table = [-int(config.frame_generator_count/2) + var for var in range(config.frame_generator_count)]
        for frame in range(config.frame_generator_count):
            new_frames = []
            for subframe in frames: 
                new_frame = subframe + new_frame_table[frame] 
                if new_frame > len(self) - 1:
                    new_frame = subframe - new_frame_table[frame] 
                new_frames.append(new_frame)  
            self.np_frames.append(self.df[config.columns].iloc[new_frames].to_numpy())

    def get_frames(self):
        frames = []
        size = self.dataframe_size() - 1
        for index in range(1, config.frames_counts + 1):
            frames.append(int((size / config.frames_counts) * index))
        return frames

    def get_unique_patientnr(self, patientgroup, patientid):
        unique = str(patientgroup)+ ','+ str(patientid)
        return unique

    def dataframe_size(self):
        return int(self.dataframe.size / len(self.dataframe.columns))

    def __len__(self):
        """
        :return: size of the df divided by the number of columns
        :rtype: int
        """
        return int(self.df.size / len(self.df.columns))
