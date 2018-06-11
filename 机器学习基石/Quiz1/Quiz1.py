import numpy as np
import pandas as pd
def loadData(filename):
    data = pd.read_csv(filename, sep='\s+', header=None)
    data = data.values
    row, col = data.shape
    X = np.c_[np.ones((row, 1)), data[:, 0 : col - 1]]
    Y = data[:, col - 1 : col]
    return X, Y
def perceptron(X, Y, weight, eta = 1):
    num = 0
    prevpos = 0
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
        weight += eta * Y[pos, 0] * X[pos : pos + 1, :].T
        num += 1
    return weight, num
X, Y = loadData('hw1_15_train.dat')
row, col = X.shape
weight = np.zeros((col, 1))
weight, num = perceptron(X, Y, weight)
print('总共更新theta的次数：',num)
total = 0
for i in range(2000):
    weight = np.zeros((col, 1))
    randops = np.random.permutation(row)
    Xrnd = X[randops, :]
    Yrnd = Y[randops, :]
    _, num = perceptron(Xrnd, Yrnd, weight)
    total += num
print('2000次平均每次更新theta的次数：',total/2000)
total = 0
for i in range(2000):
    weight = np.zeros((col, 1))
    randops = np.random.permutation(row)
    Xrnd = X[randops, :]
    Yrnd = Y[randops, :]
    _, num = perceptron(Xrnd, Yrnd, weight, 0.5)
    total += num
print('2000次平均每次更新theta的次数：',total/2000)

X, Y = loadData('hw1_18_train.dat')
Xtest, Ytest = loadData('hw1_18_test.dat')
row, col = X.shape
def mistake(yhat, Y):
    row, col = Y.shape
    return np.sum(yhat != Y) / row
def pocket(X, Y, weight, iternum, eta = 1):
    yhat = np.sign(X.dot(weight))
    yhat[np.where(yhat == 0)] = -1
    eold = mistake(yhat, Y)
    weightRST = np.zeros(weight.shape)
    for t in range(iternum):
        index = np.where(yhat != Y)[0]
        if not index.any():
            break;
        pos = index[np.random.permutation(len(index))[0]]
        weight += eta * Y[pos, 0] * X[pos : pos + 1, :].T
        yhat = np.sign(X.dot(weight))
        yhat[np.where(yhat == 0)] = -1
        enew = mistake(yhat, Y)
        if enew < eold:
            eold = enew
            weightRST = weight.copy()
    return weightRST, weight
    
total = 0
total50 = 0
total100 = 0
for i in range(2000):
    weight = np.zeros((col, 1))
    randops = np.random.permutation(row)
    Xrnd = X[randops, :]
    Yrnd = Y[randops, :]
    weight, weight50 = pocket(Xrnd, Yrnd, weight, 50)
    yhat = np.sign(Xtest.dot(weight))
    yhat[np.where(yhat == 0)] = -1
    err = mistake(yhat, Ytest)
    total += err
    yhat = np.sign(Xtest.dot(weight50))
    yhat[np.where(yhat == 0)] = -1
    err = mistake(yhat, Ytest)
    total50 += err
    weight = np.zeros((col, 1))
    weight, _ = pocket(Xrnd, Yrnd, weight, 100)
    yhat = np.sign(Xtest.dot(weight))
    yhat[np.where(yhat == 0)] = -1
    err = mistake(yhat, Ytest)
    total100 += err
print('迭代次数为50时，theta_pocket情况下的测试集错误率：',total/2000)
print('迭代次数为50时，theta_50情况下的测试集错误率：',total50/2000)
print('迭代次数为100时，theta_pocket情况下的测试集错误率：',total100/2000)
