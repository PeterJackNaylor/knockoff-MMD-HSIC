import numpy as np

from .kernel_tools import center, get_kernel_function


def HSIC(X, Y, kernel='gaussian', sigma=None):

    n, d = X.shape
    ny, dy = Y.shape

    assert n == ny
    assert dy == 1

    kernel, kernel_params = get_kernel_function(kernel, nfeats=sigma)

    Ky = center(kernel(Y[:, 0], **kernel_params))

    hsic_stats = np.zeros((d, 1))

    for i in range(d):
        Kx = center(kernel(X[:, i], **kernel_params))
        hsic = np.trace(np.matmul(Kx, Ky)) / (n ** 2)
        hsic_stats[i] = hsic

    return hsic_stats
