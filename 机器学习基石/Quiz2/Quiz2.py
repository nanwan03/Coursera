import math
import numpy as np
import pandas as pd

def loadData(filename):
    data = pd.read_csv(filename, sep='\s+', header=None)
    data = data.values
    row, col = data.shape
    X = np.c_[np.ones((row, 1)), data[:, 0 : col - 1]]
    Y = data[:, col - 1 : col]
    return X, Y
def generateData(num):
    x = np.random.uniform(-1, 1, num)
    y = np.sign(x)
    y[y == 0] = -1
    prop = np.random.uniform(0, 1, num)
    y[prop >= 0.8] *= -1
    return x, y
def decision_stump(X, Y):
    theta = np.sort(X)
    num = len(theta)
    Xtemp = np.tile(X, (num, 1))
    ttemp = np.tile(np.reshape(theta, (num, 1)), (1, num))
    ypred = np.sign(Xtemp - ttemp)
    ypred[ypred == 0] = -1
    err = np.sum(ypred != Y, axis=1)
    if np.min(err) <= num-np.max(err):
        return 1, theta[np.argmin(err)], np.min(err)/num
    else:
        return -1, theta[np.argmax(err)], (num-np.max(err))/num
def decision_stump_multi(X, Y):
    row, col = X.shape
    err = np.zeros((col,))
    s = np.zeros((col,))
    theta = np.zeros((col,))
    for i in range(col):
        s[i], theta[i], err[i] = decision_stump(X[:, i], Y[:, 0])
    pos = np.argmin(err)
    return pos, s[pos], theta[pos], err[pos]
totalin = 0
totalout = 0
for i in range(5000):
    X, Y = generateData(20)
    s, theta, errin = decision_stump(X, Y)
    errout = 0.5+0.3*s*(math.fabs(theta)-1)
    totalin += errin
    totalout += errout
print('训练集平均误差: ', totalin/5000)
print('测试集平均误差: ', totalout/5000)
X, Y = loadData('hw2_train.dat')
Xtest, Ytest = loadData('hw2_test.dat')
pos, s, theta, err = decision_stump_multi(X, Y)
print('训练集误差: ', err)
ypred = s*np.sign(Xtest[:, pos]-theta)
ypred[ypred == 0] = -1
row, col = Ytest.shape
errout = np.sum(ypred != Ytest.reshape(row,))/len(ypred)
print('测试集误差: ', errout)
