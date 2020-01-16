import numpy as np
import pandas as pd
import statistics as st
import Chunk
from Direction import Direction
from enum import Enum


class Config:
    def __init__(self, steps,meandiff):
        self.steps = steps
        self.meandiff = meandiff

class ChunkFinder:
    def __init__(self, data, value, diff):
        self.data = data.values
        self.chunks = []
        self.val = value
        self.config = Config(value, diff)
        
    def FindChunk(self, start, n, lastdir ):
        
        if(n < self.data.shape[0]- self.val):
            print("----------------------------------------------------")
            print("start nieuwe chunk : " + str(n))
            if(lastdir == Direction.none):
                if(self.data[n] > np.mean(self.data[start:n+2]) - np.mean(self.data[start:n+2])*self.config.meandiff and 
                    self.data[n] < np.mean(self.data[start:n+2]) + np.mean(self.data[start:n+2])*self.config.meandiff):
                    print("current direction: same")
                    return Direction.same
                elif((self.data[n+1])-abs(self.data[n]) < 0):
                    print("current direction: down")
                    return Direction.down
                elif((self.data[n+1])-abs(self.data[n]> 0)):
                    print("current direction: up")
                    return Direction.up

            elif(lastdir != Direction.none):
                if(self.data[n] > np.mean(self.data[start:n]) - np.mean(self.data[start:n+2])*self.config.meandiff and 
                    self.data[n] < np.mean(self.data[start:n]) + np.mean(self.data[start:n+2])*self.config.meandiff):
                    print("current direction: same")
                    return Direction.same
                elif( abs(self.data[n- self.val]) - self.data[n] > 0 
                        or (abs(self.data[n-self.val+1]) - (self.data[n]) > 0 and lastdir == Direction.up)):
                    print("current direction: up")
                    return Direction.up
                elif(abs(self.data[n- self.val] -self.data[n])  < 0  
                        or (abs(self.data[n-self.val+1]) - (self.data[n]) < 0 and lastdir == Direction.down)):
                    print("current direction: down")
                    return Direction.down
        else:
            return lastdir

    def getChunks(self):
        chunkstart = 0
        n = 0
        lastdir = Direction.none
        for n, value in enumerate(self.data):
            currentdir = self.FindChunk(chunkstart, n, lastdir)
            if(lastdir != currentdir and lastdir != Direction.none):
                self.chunks.append(Chunk.Chunk(self.data[chunkstart:n],self.chunks.count,chunkstart, lastdir))
                print("chunk gemaakt met:")
                print("start op frame: "+ str(chunkstart))
                print("einde op frame: "+ str(n))
                print("Richting is : " + str(lastdir))
                print("----------------------------------------------------")
                chunkstart = n
                lastdir = Direction.none
            else:
                lastdir = currentdir
        return self.chunks

                

