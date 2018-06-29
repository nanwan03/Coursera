import math
import numpy as np
import pandas as pd
import scipy.linalg as lin
def loadData(filename):
    data = pd.read_csv(filename, sep='\s+', header=None)
    data = data.values
    col, row = data.shape
    X = np.c_[np.ones((col, 1)), data[:, 0: row-1]]
    Y = data[:, row-1:row]
    return X, Y
def mistake(X, Y, weight):
    yhat = np.sign(X.dot(weight))
    yhat[yhat == 0] = -1
    err = np.sum(yhat != Y)/len(Y)
    return err
X, Y = loadData('hw4_train.dat')
Xtest, Ytest = loadData('hw4_test.dat')
lamb = 10
row, col = X.shape
wreg = lin.pinv(X.T.dot(X)+lamb*np.eye(col)).dot(X.T).dot(Y)
ein = mistake(X, Y, wreg)
eout = mistake(Xtest, Ytest, wreg)
print('Ein: ',ein,'Eout: ',eout)

arr = np.arange(-10, 3, 1)
lamb = 10.0**arr
num =len(arr)
ein = np.zeros((num,))
eout = np.zeros((num,))
evali = np.zeros((num,))
for i in range(num):
    wreg = lin.pinv(X.T.dot(X) + lamb[i] * np.eye(col)).dot(X.T).dot(Y)
    ein[i] = mistake(X, Y, wreg)
    eout[i] = mistake(Xtest, Ytest, wreg)
out = np.c_[np.c_[np.array(lamb),ein],eout]
print('\tlambda\t\t Ein\t\t Eout')
print(out)

Xtrain = X[0:120, :]
Ytrain = Y[0:120, :]
Xval = X[120:, :]
Yval = Y[120:, :]
ein = np.zeros((num,))
eout = np.zeros((num,))
evali = np.zeros((num,))
for i in range(num):
    wreg = lin.pinv(Xtrain.T.dot(Xtrain) + lamb[i] * np.eye(col)).dot(Xtrain.T).dot(Ytrain)
    ein[i] = mistake(Xtrain, Ytrain, wreg)
    eout[i] = mistake(Xtest, Ytest, wreg)
    evali[i] = mistake(Xval, Yval, wreg)
out = np.c_[np.c_[np.c_[np.array(lamb),ein],evali],eout]
print('\tlambda\t\t  Ein\t\t  Eval\t\t  Eout')
print(out)

lambmin = lamb[np.where(evali == np.min(evali))[0][-1]]
wreg = lin.pinv(X.T.dot(X) + lambmin * np.eye(col)).dot(X.T).dot(Y)
errin = mistake(X, Y, wreg)
errout = mistake(Xtest, Ytest, wreg)
print('Ein: ',errin,'Eout: ',errout)

ein = np.zeros((num,))
eout = np.zeros((num,))
for j in range(num):
    for i in range(5):
        Xval = X[40*i:40*(i+1), :]
        Yval = Y[40*i:40*(i+1), :]
        Xtrain = np.r_[X[0:40*i, :], X[40*(i+1):, :]]
        Ytrain = np.r_[Y[0:40*i, :], Y[40*(i+1):, :]]
        wreg = lin.pinv(Xtrain.T.dot(Xtrain) + lamb[j] * np.eye(col)).dot(Xtrain.T).dot(Ytrain)
        ein[j] += mistake(Xval, Yval, wreg)
    ein[j] /= 5
out = np.c_[np.array(lamb), ein]
print('\tlambda\t\t  Ecv')
print(out)

lambmin = lamb[np.where(ein == np.min(ein))[0][-1]]
wreg = lin.pinv(X.T.dot(X) + lambmin * np.eye(col)).dot(X.T).dot(Y)
errin = mistake(X, Y, wreg)
errout = mistake(Xtest, Ytest, wreg)
print('Ein: ',errin,'Eout: ',errout)
