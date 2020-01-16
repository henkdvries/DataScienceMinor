from sklearn.linear_model import LogisticRegression
from .model import Model


class LogisticRegressionModel(Model):
    def __init__(self, data, *args, **kwargs):
        super().__init__(data)

        self.model = LogisticRegression(*args, **kwargs)
