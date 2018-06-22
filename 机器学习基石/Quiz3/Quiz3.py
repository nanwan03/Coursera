import numpy as np
import pandas as pd
import math
import scipy.linalg as lin
def generateData(num):
    x1 = np.random.uniform(-1, 1, num)
    x2 = np.random.uniform(-1, 1, num)
    X = np.c_[x1, x2]
    X = np.c_[np.ones((num, 1)), X]
    y = np.sign(np.power(x1, 2) + np.power(x2, 2) - 0.6)
    y[y == 0] = -1
    prod = np.random.uniform(0, 1, num)
    y[prod >= 0.9] *= -1
    return X, y
totalerr = 0
for i in range(1000):
    X, Y = generateData(1000)
    theta = lin.pinv(X.T.dot(X)).dot(X.T).dot(Y)
    ypred = np.sign(X.dot(theta))
    err = np.sum(ypred!=Y)/1000
    totalerr += err
print('Ein: ', totalerr/1000)

def transform(X):
    row, col = X.shape
    Xback = np.zeros((row, 6))
    Xback[:, 0:col] = X
    Xback[:, col] = X[:, 1]*X[:, 2]
    Xback[:, col+1] = X[:, 1]**2
    Xback[:, col+2] = X[:, 2]**2
    return Xback
totalerr = 0
for i in range(1000):
    X, Y = generateData(1000)
    Xtran = transform(X)
    theta = lin.pinv(Xtran.T.dot(Xtran)).dot(Xtran.T).dot(Y)
    Xtest, Ytest = generateData(1000)
    Xback = transform(Xtest)
    ypred = np.sign(Xback.dot(theta))
    err = np.sum(ypred!=Ytest)/1000
    totalerr += err
print('theta: ', theta.T)
print('Ein: ', totalerr/1000)
def sigmoid(z):
    zback = 1/(1+np.exp(-1*z))
    return zback
def logisticReg(X, Y, eta, numiter, flag=0):
    row, col = X.shape
    theta = np.zeros((col, 1))
    num = 0
    for i in range(numiter):
        if flag == 0:
            derr = (-1*X*Y).T.dot(sigmoid(-1*X.dot(theta)*Y))/row
        else:
            if num >= row:
                num = 0
            derr = -Y[num, 0]*X[num: num+1, :].T*sigmoid(-1*X[num, :].dot(theta)[0]*Y[num, 0])
            num += 1
        theta -= eta*derr
    return theta
def loadData(filename):
    data = pd.read_csv(filename, sep='\s+', header=None)
    data = data.values
    col, row = data.shape
    X = np.c_[np.ones((col, 1)), data[:, 0: row-1]]
    Y = data[:, row-1:row]
    return X, Y
def mistake(X, Y, theta):
    yhat = X.dot(theta)
    yhat[yhat > 0] = 1
    yhat[yhat <= 0] = -1
    err = np.sum(yhat != Y)/len(Y)
    return err
X, Y = loadData('hw3_train.dat')
Xtest, Ytest = loadData('hw3_test.dat')

eta = 0.001; T = 2000; flag = 0
theta = logisticReg(X, Y, eta, T, flag)
errin = mistake(X, Y, theta)
errout = mistake(Xtest, Ytest, theta)
print('Ein = ', errin,'Eout = ', errout)

eta = 0.01; T = 2000; flag = 0
theta = logisticReg(X, Y, eta, T, flag)
errin = mistake(X, Y, theta)
errout = mistake(Xtest, Ytest, theta)
print('Ein = ', errin,'Eout = ', errout)

eta = 0.001; T = 2000; flag = 1
theta = logisticReg(X, Y, eta, T, flag)
errin = mistake(X, Y, theta)
errout = mistake(Xtest, Ytest, theta)
print('Ein = ', errin,'Eout = ', errout)
