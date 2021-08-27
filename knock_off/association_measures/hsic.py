import numpy as np

from .kernel_tools import center, get_kernel_function


def HSIC(X, Y, kernel='gaussian'):

    n, d = X.shape
    ny = len(Y)

    assert n == ny

    kernel, kernel_params = get_kernel_function(kernel, nfeats=d)

    Ky = center(kernel(Y, **kernel_params))

    hsic_stats = []

    for x in X.T:
        Kx = center(kernel(x, **kernel_params))
        hsic = np.trace(np.dot(Kx.T, Ky))
        hsic_stats.append(hsic)

    return hsic_stats
