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
