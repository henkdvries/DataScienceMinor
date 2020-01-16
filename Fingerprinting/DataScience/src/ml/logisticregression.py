from sklearn.linear_model import LogisticRegression
from ml.model import Model

import numpy as np


class LogisticRegressionModel(Model):

    def __init__(self, data, config, *args, **kwargs):
        super().__init__(data, config)

        self.printconfig(kwargs)
        self.model = LogisticRegression(*args, **kwargs)
