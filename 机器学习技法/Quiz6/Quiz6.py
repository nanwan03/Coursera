import numpy as np
import pandas as pd
import scipy.linalg as lin

def loadData(filename):
    data = pd.read_csv(filename, sep='\s+', header=None)
    data = data.values
    col, row = data.shape
    X = data[:, 0: row-1]
    Y = data[:, row-1:row]
    return X, Y
def decision_stump(X, Y, thres, U):
    row, col = X.shape
    r, c = thres.shape; besterr = 1
    btheta = 0; bs = 0; index = 0
    for i in range(col):
        Yhat1 = np.sign(np.tile(X[:, i:i+1], (1, r)).T-thres[:, i:i+1]).T
        err1 = (Yhat1!=Y).T.dot(U)
        err2 = (-1*Yhat1!=Y).T.dot(U)
        s = 1 if np.min(err1) < np.min(err2) else -1
        if s == 1 and np.min(err1) < besterr:
            besterr = np.min(err1); bs = 1
            index = i; btheta = thres[np.argmin(err1), i]
        if s == -1 and np.min(err2) < besterr:
            besterr = np.min(err2); bs = -1
            index = i; btheta = thres[np.argmin(err2), i]
    return besterr, btheta, bs, index
def ada_boost(X, Y, T):
    row, col = X.shape
    U = np.ones((row, 1))/row
    Xsort = np.sort(X, 0)
    thres = (np.r_[Xsort[0:1, :] - 0.1, Xsort[0:row - 1, :]] + Xsort) / 2
    theta = np.zeros((T,)); s = np.zeros((T,));
    index = np.zeros((T,)).astype(int); alpha = np.zeros((T,))
    err = np.zeros((T,))
    for i in range(T):
        err[i], theta[i], s[i], index[i] = decision_stump(X, Y, thres, U)
        yhat = s[i]*np.sign(X[:, index[i]:index[i]+1]-theta[i])
        delta = np.sqrt((1-err[i])/err[i])
        U[yhat==Y] /= delta
        U[yhat!=Y] *= delta
        if i == T-1:
            print('sum(U): ', np.sum(U))
        alpha[i] = np.log(delta)
        U /= np.sum(U)
    print('最小的eta: ', np.min(err))
    return theta, index, s, alpha
def predict(X, theta, index, s, alpha):
    row, col = X.shape
    num = len(theta)
    ytemp = np.tile(s.reshape((1, num)), (row, 1))*np.sign(X[:, index]-theta.reshape((1, num)))
    yhat = np.sign(ytemp.dot(alpha.reshape(num, 1)))
    return yhat

X, Y = loadData('hw2_adaboost_train.dat')
Xtest, Ytest = loadData('hw2_adaboost_test.dat')
row, col = X.shape
r, c = Xtest.shape

theta, index, s, alpha = ada_boost(X, Y, 1)
Ypred = predict(X, theta, index, s, alpha)
print('Ein(g1)：', np.sum(Ypred!=Y)/row)
Ypred = predict(Xtest, theta, index, s, alpha)
print('Eout(g1)：', np.sum(Ypred!=Ytest)/r)

theta, index, s, alpha = ada_boost(X, Y, 300)
Ypred = predict(X, theta, index, s, alpha)
print('Ein(G)：', np.sum(Ypred!=Y)/r)
Ypred = predict(Xtest, theta, index, s, alpha)
print('Eout(G)：', np.sum(Ypred!=Ytest)/r)

def matK(X, X1, gamma):
    row, col =X.shape
    r, c = X1.shape
    K = np.zeros((row, r))
    for i in range(r):
        K[:, i] = np.sum((X-X1[i:i+1, :])**2, 1)
    K = np.exp(-gamma*K)
    return K
X, Y = loadData('hw2_lssvm_all.dat')
Xtrain = X[0:400, :]; Ytrain = Y[0:400, :]
Xtest = X[400:, :]; Ytest = Y[400:, :]
row, col = Xtest.shape

gamma = [32, 2, 0.125]
lamb = [0.001, 1, 1000]
Ein = np.zeros((len(gamma), len(lamb)))
Eout = np.zeros((len(gamma), len(lamb)))
for i in range(len(gamma)):
    K = matK(Xtrain, Xtrain, gamma[i])
    K2 = matK(Xtrain, Xtest, gamma[i])
    for j in range(len(lamb)):
        beta = lin.pinv(lamb[j]*np.eye(400)+K).dot(Ytrain)
        yhat = np.sign(K.dot(beta))
        Ein[i, j] = np.sum(yhat != Ytrain)/400
        yhat2 = np.sign(K2.T.dot(beta))
        Eout[i, j] = np.sum(yhat2 != Ytest)/row
print('最小的Ein: ', np.min(Ein))
print('最小的Eout: ', np.min(Eout))
