from sklearn.metrics import classification_report, accuracy_score, log_loss, multilabel_confusion_matrix, matthews_corrcoef, brier_score_loss, mean_squared_log_error, mean_squared_error, plot_confusion_matrix
import numpy as np
import os
import csv


class Model:
    def __init__(self, data: list):
        self.X_train, self.y_train, self.X_test, self.y_test = data 

    def calculate_accuracy(self):
        y_pred = self.predict(self.X_test)
        self.accuracy = accuracy_score(self.y_test, y_pred, normalize=True)
        return self.accuracy
    
    def calculate_logloss(self):
        y_pred = self.predict_proba(self.X_test)
        self.logloss = log_loss(self.y_test, y_pred, normalize= True)
        return self.logloss

    def confusion_matrix(self):
        y_pred = self.predict(self.X_test)
        confmatrix = multilabel_confusion_matrix(self.y_test, y_pred)
        return confmatrix.tolist()
    
    def plot_conf_matrix(self):
        return plot_confusion_matrix(self.model ,self.X_test, self.y_test, normalize= 'all')

    def calculate_mcc(self):
        y_pred = self.predict(self.X_test)
        self.matthews_correlation_coefficient= matthews_corrcoef(self.y_test, y_pred)
        return self.matthews_correlation_coefficient

    def calculate_RMSE(self):
        y_pred = self.predict(self.X_test)
        test = np.array(self.y_test)
        pred = np.array(y_pred)
        test = test.astype(float)
        pred = pred.astype(float)
        self.root_mean_squared_error = np.sqrt(mean_squared_error(test, pred))
        return self.root_mean_squared_error

    def calculate_RMSLE(self):
        y_pred = self.predict(self.X_test)
        test = np.array(self.y_test)
        pred = np.array(y_pred)
        test = test.astype(float)
        pred = pred.astype(float)
        self.root_mean_squared_log_error = np.sqrt(mean_squared_log_error(test,pred))       
        return self.root_mean_squared_log_error
        
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
        
    def predict_proba(self, data):
        return self.model.predict_proba(data)

    def score(self, x, y):
        return self.model.score(x, y)

    def printconfig(self, kwargs):
        for key, value in kwargs.items():
            print("{:<17} {:<17}".format(key, value))

    def retrieve_metrics(self):
        metrics = {}
        metrics["Accuracy"] = self.calculate_accuracy()
        metrics["LogLoss"] = self.calculate_logloss()
        metrics["MCC"] = self.calculate_mcc()
        metrics["RMSE"] = self.calculate_RMSE()
        metrics["RMSLE"] = self.calculate_RMSLE()
        metrics["ConfusionMatrix"] = self.confusion_matrix() 
        return metrics
