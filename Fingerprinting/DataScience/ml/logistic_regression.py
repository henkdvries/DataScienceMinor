from sklearn.linear_model import *
from .classification import *

class logistic_regression(classification):
    def __init__(self, data, **kwargs):
        super().__init__(data, **kwargs)

    def parameters(self):
        return (self.model.intercept_, self.model.coef_)

    @property
    def model(self):
        try:
            return self._model
        except:
            self._model = LogisticRegression(solver='lbfgs')
            return self._model

