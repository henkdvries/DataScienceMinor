import numpy as np
from Direction import Direction
class Chunk:
    def __init__(self, data, chunknum, exercise,direction):
        self.data = data
        self.chunknum = chunknum
        self.exercise = exercise
        self.direction = direction
        
    
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