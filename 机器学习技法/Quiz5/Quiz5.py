import numpy as np
import pandas as pd
from sklearn.svm import SVC
X = np.array([[1, 0], [0, 1], [0, -1], [-1, 0], [0, 2], [0, -2], [-2, 0]])
Y = np.array([-1, -1, -1, 1, 1, 1, 1])
clf = SVC(C=1e20, kernel='poly', degree=2, gamma=1, coef0=1, shrinking=False)
clf.fit(X, Y)
print('支撑向量：',clf.support_vectors_, '\n对应的alpha*y：', clf.dual_coef_,'\n b: ',clf.intercept_)

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
pos1 = Ytemp == 0; pos2 = Ytemp != 0
Ytemp[pos1] = 1; Ytemp[pos2] = -1
clf = SVC(C=0.01, kernel='linear', shrinking=False)
clf.fit(X, Ytemp)
print('w: ', clf.coef_, '\n |w|: ', np.linalg.norm(clf.coef_))

Ein = np.zeros((10,))
Salpha = np.zeros((10,))
clf = SVC(C=0.01, kernel='poly', degree=2, gamma=1, coef0=1, shrinking=False)
for i in range(10):
    Ytemp = Y.copy()
    pos1 = Ytemp == i; pos2 = Ytemp != i
    Ytemp[pos1] = 1; Ytemp[pos2] = -1
    clf.fit(X, Ytemp)
    Yhat = clf.predict(X)
    Ein[i] = mistake(Ytemp, Yhat)
    Salpha[i] = np.sum(np.abs(clf.dual_coef_))
out = np.c_[Ein,Salpha]
print('\tEin\t\t Sum_alpha')
print(out)


c = np.array([0.001, 0.01, 0.1, 1, 10])
nsup = np.zeros((len(c),))
eout = np.zeros((len(c),))
Ytemp = Y.copy()
pos1 = Ytemp == 0; pos2 = Ytemp != 0
Ytemp[pos1] = 1; Ytemp[pos2] = -1
Ytesttemp = Ytest.copy()
pos1 = Ytesttemp == 0; pos2 = Ytesttemp != 0
Ytesttemp[pos1] = 1; Ytesttemp[pos2] = -1
for i in range(len(c)):
    clf = SVC(C=c[i], kernel='rbf', gamma=100, shrinking=False)
    clf.fit(X, Ytemp)
    nsup[i] = np.sum(clf.n_support_)
    yhat = clf.predict(Xtest)
    eout[i] = mistake(Ytesttemp, yhat)
out = np.c_[np.c_[c,nsup],eout]
print('\tC\t\t n_suport\t eout')
print(out)

gamma1 = np.array([1, 10, 100, 1000, 10000])
eout = np.zeros((len(gamma1),))
Ytemp = Y.copy()
pos1 = Ytemp == 0; pos2 = Ytemp != 0
Ytemp[pos1] = 1; Ytemp[pos2] = -1
Ytesttemp = Ytest.copy()
pos1 = Ytesttemp == 0; pos2 = Ytesttemp != 0
Ytesttemp[pos1] = 1; Ytesttemp[pos2] = -1
for i in range(len(gamma1)):
    clf = SVC(C=0.1, kernel='rbf', gamma=gamma1[i], shrinking=False)
    clf.fit(X, Ytemp)
    yhat = clf.predict(Xtest)
    eout[i] = mistake(yhat, Ytesttemp)
out = np.c_[gamma1, eout]
print('\t gamma \t\t eout')
print(out)

evali = np.zeros((len(gamma1),))
Ytemp = Y.copy()
pos1 = Ytemp == 0; pos2 = Ytemp != 0
Ytemp[pos1] = 1; Ytemp[pos2] = -1
for i in range(len(gamma1)):
    for j in range(20):
        pos = np.random.permutation(row)
        Xval = X[pos[0:1000], :]; Yval = Ytemp[pos[0:1000]]
        Xtrain = X[pos[1000:], :]; Ytrain = Ytemp[pos[1000:]]
        clf = SVC(C=0.1, kernel='rbf', gamma=gamma1[i], shrinking=False)
        clf.fit(Xtrain, Ytrain)
        yhat = clf.predict(Xval)
        evali[i] += mistake(yhat, Yval)
out = np.c_[gamma1, evali/20]
print('\t gamma\t\t eout')
print(out)
