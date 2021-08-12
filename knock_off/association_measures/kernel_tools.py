import numpy as np


def kernel_gaussian(x, sigma):
    n = len(x)
    x_2 = np.power(x, 2)
    dist_2 = np.tile(x_2, (n, 1)) + np.tile(x_2, (n, 1)).T - 2 * np.dot(x.T, x)
    K = np.exp(-dist_2 / (2 * np.power(sigma, 2)))
    return K


def center_K(K):

    n = K.shape[0]

    H = np.eye(n, dtype=np.float32) - 1 / n * np.ones(n, dtype=np.float32)

    K = np.dot(np.dot(H, K), H)
    K = K / (np.linalg.norm(K, 'fro') + 10e-10)

    return K