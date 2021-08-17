import numpy as np


def kernel_gaussian(x1, sigma, x2=None):
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


def center_K(K):

    n = K.shape[0]

    H = np.eye(n, dtype=np.float32) - 1 / n * np.ones(n, dtype=np.float32)

    K = np.dot(np.dot(H, K), H)
    K = K / (np.linalg.norm(K, 'fro') + 10e-10)

    return K
