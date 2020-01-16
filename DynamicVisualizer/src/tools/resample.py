import tqdm
import itertools
import numpy as np
import tabulate
from config import config
import matplotlib.pyplot as plt
import pandas as pd
from scipy import signal

debug = False

def resample_excercise(exercise_df, nbsamples=100):
    df = pd.DataFrame(columns=config.columns)
    for col in config.columns:
        data = exercise_df[col].to_numpy()
        increment = (data[0] - data[-1]) / len(data)

        # week method to make the series periodic
        data2 = np.array([])
        for i in range(len(data)):
            data2 = np.append(data2, data[-1]+(i*increment))
        d = np.append(data, data2)

        datanew = signal.resample(d, nbsamples*2)
        datanew = datanew[:nbsamples]
        df[col] = datanew

        if debug:
            print(df)
            fig = plt.figure()
            plt.subplot(1, 2, 1, title="original")
            plt.plot(data, c="red")
            plt.subplot(1, 2, 2, title="resampled")
            plt.plot(datanew, c="blue")
            plt.show()
    # end for
    return df
