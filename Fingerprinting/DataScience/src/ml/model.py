from sklearn.metrics import classification_report, accuracy_score


class Model:

    def __init__(self, data: list, config):
        self.X_train, self.X_test, self.y_train, self.y_test = data
        self.config = config

    def rapport(self):
        y_pred = self.predict(self.X_test)
        self.accuracy = accuracy_score(self.y_test, y_pred, normalize=True)
        self.classification = classification_report(self.y_test, y_pred)
        print()
        print('accuracy_score:\t', self.accuracy)
        print(self.classification)

    def train(self):
        self.model.fit(self.X_train, self.y_train)

    def predict(self, data):
        return self.model.predict(data)

    def score(self, x, y):
        return self.model.score(x, y)

    def printconfig(self, kwargs):
        pass
        # for key, value in kwargs.items():
        #     print("{:<17} {:<17}".format(key, value))
