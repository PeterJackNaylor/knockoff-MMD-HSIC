import numpy as np


def get_kernel_function(name, nfeats=1):
    if name == 'gaussian':
        kernel = kernel_gaussian
        kernel_params = {'sigma': np.sqrt(nfeats)}
    else:
        raise "No valid kernel."

    return kernel, kernel_params


def kernel_gaussian(x1, x2=None, sigma=1):

    if len(x1.shape) == 1:
        x1 = np.expand_dims(x1, axis=1)

    x1_2 = np.power(x1, 2)

    if x2 is not None:
        if len(x2.shape) == 1:
            x2 = np.expand_dims(x2, axis=1)
        x2_2 = np.power(x2, 2)
    else:
        x2 = x1
        x2_2 = x1_2

    dist_2 = x2_2 + x1_2.T - 2 * np.dot(x1, x2.T)
    K = np.exp(-dist_2 / (2 * np.power(sigma, 2)))
    return K


def center(K):

    n, d = K.shape

    assert n == d

    H = np.eye(n) - 1 / n * np.ones((n, n))
    KH = np.matmul(K, H)

    return KH
