import numpy as np
import pandas as pd
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.datasets import load_iris, load_boston
from .helper import *
import matplotlib.pyplot as plt

class Data:
    def __init__(self, train_X, train_y, valid_X, valid_y, label_X, label_y, degree=1, bias=False, column_y = False, scale=False, f_y=None):
        self._train_X = train_X
        self._train_y = train_y
        self._valid_y = valid_y if len(valid_X) > 0 else train_y
        self._valid_X = valid_X if len(valid_X) > 0 else train_X
        self._label_X = label_X
        self.label_y = label_y
        self._degree = degree
        self._bias = bias
        self._scale = scale
        self.f_y = f_y
        self._column_y = column_y

    def train(self):
        return zip(self.train_X, self.train_y)

    def valid(self):
        return zip(self.valid_X, self.valid_y)

    def thresholds(self, t):
        train_y = thresholds(self.train_y, t)
        valid_y = thresholds(self.valid_y, t)
        return Data(self._train_X, train_y, self._valid_X, valid_y, self.label_X, self.label_y, degree=self.degree, bias=self.bias)

    @property
    def column_y(self):
        return self._column_y

    @column_y.setter
    def column_y(self, value):
        try:
            del self._train_ty
        except: pass
        try:
            del self._valid_ty
        except: pass
        self._column_y = value

    @property
    def degree(self):
        return self._degree

    @degree.setter
    def degree(self, value):
        self._degree = value
        try:
            del self._train_tX
        except: pass
        try:
            del self._valid_tX
        except: pass

    @property
    def bias(self):
        return self._bias

    @bias.setter
    def bias(self, value):
        self._bias = value
        try:
            del self._train_tX
        except: pass
        try:
            del self._valid_tX
        except: pass
        try:
            del self._label_tX
        except: pass

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        try:
            del self._train_tX
        except: pass
        try:
            del self._valid_tX
        except: pass

    def polyX(self, X):
        if self.degree > 1:
            return polynomials(X, self.degree)
        else:
            return X

    def scaleX(self, X):
        X = self.polyX(X)
        if self._scale:
            try:
                self._scaler
            except:
                self._scaler = StandardScaler()
                self._scaler.fit(self.polyX(self._train_X))
            return self._scaler.transform(X)
        else:
            return X

    def transformed_y(self, y):
        y = np.asarray(y)
        if self.f_y is not None:
            y = self.f_y(y)
        return y

    def transform_y(self, y):
        y = self.transformed_y(y)
        if self.column_y:
            y = np.expand_dims(y, axis=1)
        return y

    @property
    def label_X(self):
        try:
            return self._label_tX
        except:
            if self.bias:
                self._label_tX = ['bias']
                self._label_tX.extend(self._label_X)
            else:
                self._label_tX = self._label_X
            return self._label_tX

    def transform_X(self, X):
        X = self.scaleX(X)
        if self.bias:
            return np.hstack([np.ones((X.shape[0], 1)), X])
        return X

    @property
    def train_X(self):
        try:
            return self._train_tX
        except:
            self._train_tX = self.transform_X(self._train_X)
            return self._train_tX

    @property
    def valid_X(self):
        try:
            return self._valid_tX
        except:
            self._valid_tX = self.transform_X(self._valid_X)
            return self._valid_tX

    def train_X_interpolated(self, factor=2):
        if factor == 0:
            return self.train_X
        X = order_x(self._train_X)
        for i in range(factor):
            X = np.append( X, np.array([ (x1 + x2) / 2 for x1, x2 in zip(X[:-1], X[1:]) ] ), axis=0)
            X = order_x(X)
        return self.transform_X(X)

    def valid_X_interpolated(self, factor=2):
        if factor == 0:
            return self.valid_X
        X = order_x(self._valid_X)
        for i in range(factor):
            X = np.append( X, np.array([ (x1 + x2) / 2 for x1, x2 in zip(X[:-1], X[1:]) ] ), axis=0)
            X = order_x(X)
        return self.transform_X(X)

    @property
    def train_y(self):
        try:
            return self._train_ty
        except:
            self._train_ty = self.transform_y(self._train_y)
            return self._train_ty

    @property
    def valid_y(self):
        try:
            return self._valid_ty
        except:
            self._valid_ty = self.transform_y(self._valid_y)
            return self._valid_ty

    def _plot(self, x, y = None, xlabel='', ylabel=None, marker='.' ):
        if y is None:
            y = self.transformed_y(self._train_y)
        plt.scatter(x, y, marker=marker)
        if ylabel is None:
            plt.ylabel(self.label_y)
        else:
            plt.ylabel(ylabel)
        plt.xlabel(xlabel)

    def plot(self, x = 0, y = None, xlabel = None, **kwargs ):
        if xlabel is None:
            xlabel = self.label_X[x]
        self._plot( self.train_X[:, x], y, xlabel, **kwargs )

    def plot_valid(self, x = 0, y = None, xlabel = None, **kwargs ):
        if xlabel is None:
            xlabel = self.label_X[x]
        self._plot( self.valid_X[:, x], self.valid_y, xlabel, **kwargs )

    def plot2d(self, markersize=4, x1=0, x2=1, y=None, loc='upper right'):
        if y == None:
            y = self.transformed_y(self._train_y)
        for c in sorted(np.unique(y)):
            x = self.train_X[c == y]
            plt.plot(x[:, x1], x[:, x2], '.', markersize=markersize, label=int(c))
        plt.ylabel(self.label_X[x2])
        plt.xlabel(self.label_X[x1])
        plt.gca().legend(loc=loc)

    @classmethod
    def from_dataframe(cls, dataframe, target, *features, **kwargs):
        features = [f for f in features if f is not None]
        if len(features) == 0:
            features = dataframe.columns.difference([target])
        X = np.array(dataframe[features]) 
        y = dataframe[target]
        return cls.from_numpy(X, y, target, features, **kwargs)

    @classmethod
    def from_numpy(cls, X, y, target, features, valid_perc=0.2, random_state=3, **kwargs):
        X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=valid_perc, random_state=random_state)
        return cls(X_train, y_train, X_valid, y_valid, features, target, **kwargs)

def thresholds(y, thresholds):
    yn = np.zeros(y.shape)
    for t in thresholds:
        yn += (y >= t) * 1
    return yn

def autompg_pd():
    df = pd.read_csv('/data/datasets/auto-mpg.csv', delimiter=',')
    df = df[df['horsepower'] != '?']
    df['horsepower'] = df['horsepower'].astype(int)
    return df

def autompg(*features, **kwargs):
    df = autompg_pd()
    if len(features) == 0:
        features = ['cylinders', 'displacement', 'horsepower', 'weight', 'acceleration']
    return Data.from_dataframe( df, 'mpg', *features, **kwargs )

def bigmart_pd():
    df = pd.read_csv('/data/datasets/bigmartdatasales.csv', delimiter=',')
    return df

def bigmart(*features, **kwargs):
    df = bigmart_pd()
    return Data.from_dataframe( df, 'Item_Outlet_Sales', *features, **kwargs )

def advertising_pd():
    df = pd.read_csv('/data/datasets/advertising.csv', delimiter=',')
    # this is fiction, just pretend that we can compute something as profit
    # based on sales - costs for the purpose of demonstrating polynomial regression
    df['Profit'] = df.Sales * 20 - df.TV - df.Radio - df.Newspaper - 50
    return df

def advertising(target, *features, **kwargs):
    transform_y = kwargs.pop('transform_y', None)
    df = advertising_pd()
    df = df.drop(columns=['Sales' if target == 'Profit' else 'Profit'])
    data = Data.from_dataframe( df, target, *features, **kwargs )
    if transform_y is not None:
        return data.transform_y(transform_y)
    return data

def advertising_sales_tv(**kwargs):
    return advertising('Sales', 'TV', **kwargs)

def advertising_profit_tv(**kwargs):
    return advertising('Profit', 'TV', **kwargs)

def advertising_profit_classify(**kwargs):
    return advertising('Profit', 'TV', 'Radio', transform_y = lambda y: (y > 0) * 1)

def advertising_sales_radio(**kwargs):
    return advertising('Sales', 'Radio', **kwargs)

def advertising_sales_newspaper(**kwargs):
    return advertising('Sales', 'Newspaper', **kwargs)

def advertising_sales(**kwargs):
    return advertising('Sales', **kwargs)

def iris_pd():
    iris=load_iris()
    df = pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                      columns= iris['feature_names'] + ['target'])
    return df

def boston_pd():
    boston=load_boston()
    features = np.array([x.lower() for x in boston.feature_names])
    df = pd.DataFrame(data=boston.data, columns=features)
    df['price'] = pd.Series(boston.target)
    return df

def boston_lstat(**kwargs):
    return Data.from_dataframe(boston_pd(), 'price', 'lstat', **kwargs)

def boston(*features, **kwargs):
    return Data.from_dataframe(boston_pd(), 'price', *features, **kwargs)

def iris_binary_pd():
    df = iris_pd()
    df = df[df.target > 0]
    df.target -= 1
    return df

def iris_classify(**kwargs):
    return Data.from_dataframe( iris_binary_pd(), 'target', 'petal length (cm)', 'petal width (cm)', **kwargs)

def titanic_pd():
    df = pd.read_csv('/data/datasets/titanic.csv', delimiter=',')
    df.Sex = (df.Sex == 'male') * 1
    df = df[['Survived', 'Pclass','Sex', 'Age', 'SibSp','Parch', 'Fare']]
    df = df.dropna()
    return df

def titanic(*features, **kwargs):
    return Data.from_dataframe( titanic_pd(), 'Survived', *features, **kwargs )

def liver_pd():
    df = pd.read_csv('/data/datasets/indian_liver_patient.csv', delimiter=',')
    df.Gender = (df.Gender == 'Male') * 1
    df = df.rename(columns={'Dataset':'Disease'})
    df.Disease = df.Disease - 1
    df = df.dropna()
    return df

def liver(*features, **kwargs):
    return Data.from_dataframe( liver_pd(), 'Disease', *features, **kwargs )

def wines_pd():
    return pd.read_csv('/data/datasets/winequality-red.csv', delimiter=';')

def wines_binary(target, *features, threshold=6, **kwargs):
    return wines(target, *features, f_y=lambda y: (y >= threshold) * 1, **kwargs)

def wines_multi_class(target, thresholds, *features, **kwargs):
    return wines(target, *features, **kwargs).thresholds(thresholds)

def wines(target, *features, **kwargs):
    transform_y = kwargs.pop('transform_y', None)
    data = Data.from_dataframe( wines_pd(), target, *features, **kwargs )
    if transform_y is not None:
        return data.transform_y(transform_y)
    return data

def wines_quality_alcohol(**kwargs):
    return wines('quality', 'alcohol', **kwargs)

def polynomials(X, degree):
    poly = PolynomialFeatures(degree, include_bias=False)
    return poly.fit_transform(X)

def dam(**kwargs):
    with open("/data/datasets/dam_water_data.pickle", "rb") as myfile:
        X_train, X_val, X_test, X_all, y_train, y_val, y_test, y_all = pickle.load(myfile)
    target = 'Hydrostatics of a dam'
    features = ['Outflow of water']

    if 'random_state' in kwargs or 'valid_perc' in kwargs:
        return Data.from_numpy(X_all, y_all, target, features, **kwargs)
    return Data(X_train, y_train, X_val, y_val, ['Outflow of water'], 'Hydrostatics of a dam', **kwargs)
