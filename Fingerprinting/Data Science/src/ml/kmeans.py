from sklearn.cluster import KMeans
import numpy as np 
from models.visualisation import Visualisation

class KMeansModel(): 
    def __init__(self,n_clusters=2, random_state=0):
        self.model = KMeans(n_clusters=n_clusters, random_state=random_state)
        #self.KMeans= KMeans(n_clusters=2)

    def train(self, x):
        #print('[train()] gamma: {gamma}, kernel: {kernel}, C: {C}, impl: {_impl}'.format(gamma=self.clf.gamma, kernel=self.clf.kernel, C=self.clf.C, _impl=self.clf._impl))
        self.model.fit(x)
        print('test')

    def predict(self, data):
        return self.model.predict(data)

    def test(self, x, y):
        if len(x) != len(y):
            raise ValueError('Status values need to be same lenghts')
        score = self.model.score(x, y)
        print('[test()] clf.score:', score, 'from', len(x), 'test records')

        wrong = 0 
        array = []  
        for i in range(len(x)):
            if self.predict([x[i]]) != y[i]:
                wrong = wrong + 1
            array.append(self.predict([x[i]]))
        print(wrong, len(x))
        return np.array(array), y 
    
    def visualse(self, x, y):
        Visualisation(x, y, self).show()
    