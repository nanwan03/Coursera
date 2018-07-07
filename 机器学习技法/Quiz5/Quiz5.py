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
X, Y = loadData('features_train.dat')
Xtest, Ytest = loadData('features_test.dat')

row, col = X.shape
Ytemp = Y.copy()
pos1 = Ytemp == 0
pos2 = Ytemp != 0
Ytemp[pos1] = 1
Ytemp[pos2] = -1
clf = SVC(C=0.01, kernel='linear', shrinking=False)
clf.fit(X, Ytemp)
print(np.linalg.norm(clf.coef_))

Ein = np.zeros((5, ))
alpha = np.zeros((5, ))
clf = SVC(C=0.01, kernel = 'poly', degree = 2, gamma = 1, coef0 = 1, shrinking = False)
for i in range(0, 5):
    Ytemp = Y.copy()
    pos1 = Ytemp == i * 2
    pos2 = Ytemp != i * 2
    Ytemp[pos1] = 1
    Ytemp[pos2] = -1
    clf.fit(X, Ytemp)
    yhat = clf.predict(X)
    Ein[i] = mistake(yhat, Ytemp)
    alpha[i] = np.sum(np.abs(clf.dual_coef_))
print(np.argmin(Ein) * 2)
print(np.max(alpha))

gamma = np.array([1, 10, 100, 1000, 10000])
eout = np.zeros((len(gamma),))
Ytemp = Y.copy()
pos1 = Ytemp == 0
pos2 = Ytemp != 0
Ytemp[pos1] = 1
Ytemp[pos2] = -1
Ytesttemp = Ytest.copy()
pos1 = Ytesttemp == 0
pos2 = Ytesttemp != 0
Ytesttemp[pos1] = 1
Ytesttemp[pos2] = -1
for i in range(len(gamma)):
    clf = SVC(C=0.1, kernel='rbf', gamma=gamma[i], shrinking=False)
    clf.fit(X, Ytemp)
    yhat = clf.predict(Xtest)
    eout[i] = mistake(yhat, Ytesttemp)
print(gamma[np.argmin(eout)])

evali = np.zeros((len(gamma),))
Ytemp = Y.copy()
pos1 = Ytemp == 0
pos2 = Ytemp != 0
Ytemp[pos1] = 1
Ytemp[pos2] = -1
for i in range(len(gamma)):
    for j in range(5):
        pos = np.random.permutation(row)
        Xval = X[pos[0:1000], :]
        Yval = Ytemp[pos[0:1000]]
        Xtrain = X[pos[1000:], :]
        Ytrain = Ytemp[pos[1000:]]
        clf = SVC(C=0.1, kernel='rbf', gamma=gamma[i], shrinking=False)
        clf.fit(Xtrain, Ytrain)
        yhat = clf.predict(Xval)
        evali[i] += mistake(yhat, Yval)
    evali[i] /= 5
print(gamma[np.where(evali == np.min(evali))[0][0]])
