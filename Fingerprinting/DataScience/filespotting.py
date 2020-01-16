import numpy as np
import pandas as pd 
from tabulate import tabulate
import Chunk
import ChunkFinder
from Direction import Direction
import matplotlib.pyplot as plt

class Chunk:
    def __init__(self, data, chunknum, exercise):
        self.data = data
        self.chunknum = chunknum
        self.exercise = exercise
        
    
    def getdescriptive(self):
        descriptives = {'sum':{},'mean':{},'count':{}, 'min':{}, 'max':{},'begin':{},'end':{}}
        
        descriptives['sum'] = {column: self.data[[column]].sum() for column in self.data.columns}
        
        descriptives['mean'] = {column : np.mean(self.data[[column]]) for column in self.data.columns}
    
        descriptives['count'] = {column : len(self.data[[column]]) for column in self.data.columns}
        
        descriptives['min'] = {column : self.data[[column]].min() for column in self.data.columns}
        descriptives['max'] = {column : self.data[[column]].max() for column in self.data.columns}
        descriptives['begin'] = {column : self.data[[column]].iloc[:1,] for column in self.data.columns}
        descriptives['end'] = {column : self.data[[column]].iloc[-1] for column in self.data.columns}

        return descriptives



differences = []
path = "C:/Users/lennart/Desktop/DataScienceMinor/filespotting/"

mapdir1 = "bad"
mapdir2 = "good"

dataframe = pd.read_csv(path + mapdir1 + "/" + "AB1" + ".csv" ,names=list(range(30)), skipinitialspace=True)
columns = {0: "thorax_r_x", 1: "thorax_r_y", 2: "thorax_r_z",
                     3: "clavicula_r_x", 4: "clavicula_r_y",
                     5: "clavicula_r_z",
                     6: "scapula_r_x", 7: "scapula_r_y", 8: "scapula_r_z",
                     9: "humerus_r_x", 10: "humerus_r_y", 11: "humerus_r_z",
                     12: "ellebooghoek_r",
                     15: "thorax_l_x", 16: "thorax_l_y", 17: "thorax_l_z",
                     18: "clavicula_l_x", 19: "clavicula_l_y",
                     20: "clavicula_l_z",
                     21: "scapula_l_x", 22: "scapula_l_y", 23: "scapula_l_z",
                     24: "humerus_l_x", 25: "humerus_l_y", 26: "humerus_l_z",
                     27: "ellebooghoek_l"}

dataframe = dataframe.rename(columns= columns)
finder = ChunkFinder.ChunkFinder(dataframe["humerus_r_x"], 2, 0.10)

dataframechunks = finder.getChunks()

print("zoveel chunks zijn er: " + str(len(dataframechunks)))

fig, ax = plt.subplots()
ax.plot(dataframe['humerus_r_x'])
ax.set_xlim(0)
ymin = min(dataframe['humerus_r_x'])
ymax = max(dataframe['humerus_r_x'])
for x in dataframechunks:
    if(x.direction == Direction.down):
        ax.vlines(x.exercise,ymin,ymax , lw = 2, color = 'r', label = x.chunknum)
    if(x.direction == Direction.up):
        ax.vlines(x.exercise,ymin,ymax , lw = 2, color = 'g', label = x.chunknum)
    if(x.direction == Direction.same):
        ax.vlines(x.exercise,ymin,ymax , lw = 2, color = 'b', label = x.chunknum)

plt.show()
