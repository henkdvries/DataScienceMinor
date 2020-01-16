from sklearn.neural_network import MLPClassifier
from models.model import Model

class MLPClassifierModel(Model):

    def __init__(self, data, *args, **kwargs):
        super().__init__(data)

        # self.printconfig(kwargs)
        self.model = MLPClassifier(*args, **kwargs)
