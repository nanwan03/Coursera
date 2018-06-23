import numpy as np
import pandas as pd
import math
import scipy.linalg as lin

def generateData(num):
    x1 = np.random.uniform(-1, 1, num)
    x2 = np.random.uniform(-1, 1, num)
    X = np.c_[x1, x2]
    X = np.c_[np.ones((num, 1)), X]
    y = np.sign(x1 ** 2 + x2 ** 2 - 0.6)
    y[y == 0] = -1
    prod = np.random.uniform(0, 1, num)
    y[prod >= 0.9] *= -1
    return X, y
totalerr = 0
for i in range(1000):
    X, Y = generateData(1000)
    theta = lin.pinv(X.T.dot(X)).dot(X.T).dot(Y)
    ypred = np.sign(X.dot(theta))
    ypred[ypred == 0] = -1
    err = np.sum(ypred != Y) / 1000
    totalerr += err
print('Ein: ', totalerr/1000)

def transform(X):
    row, col = X.shape
    Xrst = np.zeros((row, 6))
    Xrst[:, 0 : col] = X
    Xrst[:, col] = X[:, 1] *X[:, 2]
    Xrst[:, col + 1] = X[:, 1] ** 2
    Xrst[:, col + 2] = X[:, 2] ** 2
    return Xrst
totalerr = 0
for i in range(1000):
    X, Y = generateData(1000)
    Xtran = transform(X)
    weight = lin.pinv(Xtran.T.dot(Xtran)).dot(Xtran.T).dot(Y)
    Xtest, Ytest = generateData(1000)
    Xback = transform(Xtest)
    ypred = np.sign(Xback.dot(weight))
    ypred[ypred == 0] = -1
    err = np.sum(ypred != Ytest) / 1000
    totalerr += err
print('weight: ', weight.T)
print('Ein: ', totalerr/1000)

def loadData(filename):
    data = pd.read_csv(filename, sep='\s+', header=None)
    data = data.values
    col, row = data.shape
    X = np.c_[np.ones((col, 1)), data[:, 0: row-1]]
    Y = data[:, row-1:row]
    return X, Y
def sigmoid(z):
    return 1 / (1 + np.exp(-1 * z))
def mistake(X, Y, weight):
    row, col = Y.shape
    yhat = np.sign(X.dot(weight))
    yhat[yhat == 0] = -1
    return np.sum(yhat != Y) / row
def logisticReg(X, Y, eta, iternum = 2000, flag = 0):
    row, col = X.shape
    weight = np.zeros((col, 1))
    num = 0
    for t in range(iternum):
        if flag == 0:
            derr = (X * Y).T.dot(sigmoid(-1 * X.dot(weight) * Y)) / row
        else:
            if num >= row:
                num = 0
            derr = (X[num : num + 1, :] * Y[num, 0]).T.dot(sigmoid(-1 * X[num, :].dot(weight)[0] * Y[num, 0]))
            num += 1
        weight += eta * derr
    return weight
X, Y = loadData('hw3_train.dat')
Xtest, Ytest = loadData('hw3_test.dat')

weight = logisticReg(X, Y, 0.001)
errin = mistake(X, Y, weight)
errout = mistake(Xtest, Ytest, weight)
print('Ein = ', errin,'Eout = ', errout)

eta = 0.01; T = 2000; flag = 0
weight = logisticReg(X, Y, 0.01)
errin = mistake(X, Y, weight)
errout = mistake(Xtest, Ytest, weight)
print('Ein = ', errin,'Eout = ', errout)

weight = logisticReg(X, Y, 0.001, 2000, 1)
errin = mistake(X, Y, weight)
errout = mistake(Xtest, Ytest, weight)
print('Ein = ', errin,'Eout = ', errout)
