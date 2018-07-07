import numpy as np
import pandas as pd
from sklearn.svm import SVC
X = np.array([[1, 0], [0, 1], [0, -1], [-1, 0], [0, 2], [0, -2], [-2, 0]])
Y = np.array([-1, -1, -1, 1, 1, 1, 1])
clf = SVC(C = 1e20, kernel = 'poly', degree = 2, gamma = 1, coef0 = 1, shrinking = False)
clf.fit(X, Y)
print(clf.support_vectors_)
print(clf.dual_coef_)
print(clf.intercept_)

def loadData(filename):
    data = pd.read_csv(filename, sep='\s+', header=None)
    data = data.values
    col, row = data.shape
    X = np.c_[np.ones((col, 1)), data[:, 1: row]]
    Y = data[:, 0]
    return X, Y
def mistake(yhat, y):
    err = np.sum(yhat != y)/len(y)
    return err
def transform(Y, target):
    Ytest = Y.copy()
    pos1 = Y == target
    pos2 = Y != target
    Ytest[pos1] = 1
    Ytest[pos2] = -1
    return Ytest
X, Y = loadData('features_train.dat')
Xtest, Ytest = loadData('features_test.dat')

row, col = X.shape
Ytemp = transform(Y, 0)
clf = SVC(C=0.01, kernel='linear', shrinking=False)
clf.fit(X, Ytemp)
print(np.linalg.norm(clf.coef_))

Ein = np.zeros((5, ))
alpha = np.zeros((5, ))
clf = SVC(C=0.01, kernel = 'poly', degree = 2, gamma = 1, coef0 = 1, shrinking = False)
for i in range(0, 5):
    Ytemp = transform(Y, i * 2)
    clf.fit(X, Ytemp)
    yhat = clf.predict(X)
    Ein[i] = mistake(yhat, Ytemp)
    alpha[i] = np.sum(np.abs(clf.dual_coef_))
print(np.argmin(Ein) * 2)
print(np.max(alpha))

gamma = np.array([1, 10, 100, 1000, 10000])
eout = np.zeros((len(gamma),))
Ytemp = transform(Y, 0)
Ytesttemp = transform(Ytest, 0)
for i in range(len(gamma)):
    clf = SVC(C=0.1, kernel = 'rbf', gamma = gamma[i], shrinking=False)
    clf.fit(X, Ytemp)
    yhat = clf.predict(Xtest)
    eout[i] = mistake(yhat, Ytesttemp)
print(gamma[np.argmin(eout)])

Ytemp = transform(Y, 0)
evali = 0
for i in range(100):
    randops = np.random.permutation(row)
    Xval = X[randops[0:1000], :]
    Yval = Ytemp[randops[0:1000]]
    Xtrain = X[randops[1000:], :]
    Ytrain = Ytemp[randops[1000:]]
    clf = SVC(C=0.1, kernel='rbf', gamma=10, shrinking=False)
    clf.fit(Xtrain, Ytrain)
    yhat = clf.predict(Xval)
    evali += mistake(yhat, Yval)
evali /= 100
print(evali)
