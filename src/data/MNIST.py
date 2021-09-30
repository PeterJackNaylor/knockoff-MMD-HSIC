#!/usr/bin/env python

from mnist import train_images, train_labels
import numpy as np

def get_X(num):
    label = train_labels()
    
    X = train_images()
    X = X[label == num, ]
    X = X.reshape(-1, 784)
    
    return X

threes = get_X(3)[:6131,]
sevens = get_X(7)[:6131,]

assert threes.shape == (6131, 784)
assert sevens.shape == (6131, 784)

X = np.concatenate((threes, sevens), axis=0)
X = (X - X.mean()) / X.std()

y = np.zeros(X.shape[0])
y[sevens.shape[0]:] = 1

np.savez("Xy.npz", X=X, Y=y)
np.savez("avg_number.npz",
         three=threes.sum(axis=0),
         seven=sevens.sum(axis=0))
