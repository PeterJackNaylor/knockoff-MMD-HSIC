#!/usr/bin/env python

from mnist import train_images, train_labels
import numpy as np

def get_X(num):
    label = train_labels()
    
    X = train_images()
    X = X[label == num, ]
    X = X.reshape(-1, 784)
    
    return X

threes = get_X(3)[:200,]
sevens = get_X(7)[:200,]

assert threes.shape == (200, 784)

X = np.concatenate((threes, sevens), axis=0)
X = (X - X.mean()) / X.std()

y = np.zeros(X.shape[0])
y[sevens.shape[0]:] = 1

np.savez("Xy.npz", X=X, Y=y)
