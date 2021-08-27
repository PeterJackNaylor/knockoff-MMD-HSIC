import numpy as np


def get_kernel_function(name, nfeats=1):
    if name == 'gaussian':
        kernel = kernel_gaussian
        kernel_params = {'sigma': np.sqrt(nfeats)}
    else:
        raise "No valid kernel."

    return kernel, kernel_params


def kernel_gaussian(x1, x2=None, sigma=1):
    n = len(x1)
    x1_2 = np.power(x1, 2)
    x1_2 = np.tile(x1_2, (n, 1))

    if x2 is not None:
        x2_2 = np.power(x2, 2)
        x2_2 = np.tile(x2_2, (n, 1))
    else:
        x2 = x1
        x2_2 = x1_2

    dist_2 = x2_2 + x1_2.T - 2 * np.dot(x1.T, x2)
    K = np.exp(-dist_2 / (2 * np.power(sigma, 2)))
    return K


def center(mat):

    n = mat.shape[0]

    H = np.eye(n) - 1 / n * np.ones([n, n])
    mat = np.dot(np.dot(H, mat), H)
    mat = mat / (np.linalg.norm(mat, 'fro') + 10e-10)

    return mat
