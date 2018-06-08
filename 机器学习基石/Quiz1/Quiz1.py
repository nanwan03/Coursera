import numpy as np
import pandas as pd
def loadData(filename):
    data = pd.read_csv(filename, sep='\s+', header=None)
    data = data.values
    col, row = data.shape
    X = np.c_[np.ones((col, 1)), data[:, 0: row-1]]
    Y = data[:, row-1:row]
    return X, Y
def perceptron(X, Y, weight, eta=1):
    num = 0; prevpos = 0
    while(True):
        yhat = np.sign(X.dot(weight))
        yhat[np.where(yhat == 0)] = -1
        index = np.where(yhat != Y)[0]
        if not index.any():
            break
        if not index[index >= prevpos].any():
            prevpos = 0
        pos = index[index >= prevpos][0]
        prevpos = pos
        weight += eta*Y[pos, 0]*X[pos:pos+1, :].T
        num += 1
    return weight, num
X, Y = loadData('hw1_15_train.dat')
col, row = X.shape
weight = np.zeros((row, 1))
weight, num = perceptron(X, Y, weight)
print('总共更新theta的次数：',num)
total = 0
for i in range(2000):
    weight = np.zeros((row, 1))
    randpos = np.random.permutation(col)
    Xrnd = X[randpos, :]
    Yrnd = Y[randpos, :]
    _, num = perceptron(Xrnd, Yrnd, weight)
    total += num
print('2000次平均每次更新theta的次数：',total/2000)
total = 0
for i in range(2000):
    weight = np.zeros((row, 1))
    randpos = np.random.permutation(col)
    Xrnd = X[randpos, :]
    Yrnd = Y[randpos, :]
    _, num = perceptron(Xrnd, Yrnd, weight, 0.5)
    total += num
print('2000次平均每次更新theta的次数：',total/2000)

X, Y = loadData('hw1_18_train.dat')
Xtest, Ytest = loadData('hw1_18_test.dat')
col, row = X.shape
weight = np.zeros((row, 1))
def mistake(yhat, y):
    row, col = y.shape
    return np.sum(yhat != y)/row
def pocket(X, Y, weight, iternum, eta = 1):
    yhat = np.sign(X.dot(weight))
    yhat[np.where(yhat == 0)] = -1
    errold = mistake(yhat, Y)
    weightRST = np.zeros(weight.shape)
    for t in range(iternum):
        index = np.where(yhat != Y)[0]
        if not index.any():
            break
        pos = index[np.random.permutation(len(index))[0]]
        weight += eta * Y[pos, 0] * X[pos:pos + 1, :].T
        yhat = np.sign(X.dot(weight))
        yhat[np.where(yhat == 0)] = -1
        errnow = mistake(yhat, Y)
        if errnow < errold:
            weightRST = weight.copy()
            errold = errnow
    return weightRST, weight
total = 0
total50 = 0
for i in range(2000):
    weight = np.zeros((row, 1))
    randpos = np.random.permutation(col)
    Xrnd = X[randpos, :]
    Yrnd = Y[randpos, 0:1]
    weight, weightCur = pocket(Xrnd, Yrnd, weight, 50)
    yhat = np.sign(Xtest.dot(weight))
    yhat[np.where(yhat == 0)] = -1
    err = mistake(yhat, Ytest)
    total += err
    yhat = np.sign(Xtest.dot(weightCur))
    yhat[np.where(yhat == 0)] = -1
    err = mistake(yhat, Ytest)
    total50 += err
print('迭代次数为50时，theta_pocket情况下的测试集错误率：',total/2000)
print('迭代次数为50时，theta_50情况下的测试集错误率：',total50/2000)
total = 0
for i in range(2000):
    weight = np.zeros((row, 1))
    randpos = np.random.permutation(col)
    Xrnd = X[randpos, :]
    Yrnd = Y[randpos, 0:1]
    weight, _ = pocket(Xrnd, Yrnd, weight, 100)
    yhat = np.sign(Xtest.dot(weight))
    yhat[np.where(yhat == 0)] = -1
    err = mistake(yhat, Ytest)
    total += err
print('迭代次数为100时，theta_pocket情况下的测试集错误率：',total/2000)
