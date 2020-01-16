import matplotlib.pyplot as plt

from sklearn.preprocessing import PolynomialFeatures
from sklearn import svm
import numpy as np
from ml.model import Model


class SVCModel(Model):

    def __init__(self, data, config, *args, **kwargs):
        super().__init__(data, config)

        self.printconfig(kwargs)

        self.model = svm.SVC(*args, **kwargs)

    def polynomials(self, X, degree):
        poly = PolynomialFeatures(degree, include_bias=False)
        return poly.fit_transform(X)

    def plot_boundary(self, h=0.01):
        ax = plt.gca()
        x_min, x_max = ax.get_xlim()
        y_min, y_max = ax.get_ylim()
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h),
                             np.arange(y_min, y_max, h))
        X = np.matrix(np.vstack([xx.ravel(), yy.ravel()])).T
        if self.data.degree > 1:
            X = self.polynomials(X, self.data.degree)
        boundary = self.predict(X)
        boundary = boundary.reshape(xx.shape)
        ax.contour(xx, yy, boundary)
