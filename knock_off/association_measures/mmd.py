import numpy as np

from .kernel_tools import get_kernel_function


def MMD(X, Y, kernel='gaussian'):

    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1

    kernel, kernel_params = get_kernel_function(kernel, nfeats=d)

    Ky = kernel(Y[:, 0], **kernel_params)
    mmd_stats = np.zeros((d, 1))

    for i in range(d):
        Kx = kernel(X[:, i], **kernel_params)
        Kxy = kernel(X[:, i], Y[:, 0], **kernel_params)

        # set diagonal to 0?
        mmd = (Kx + Ky - 2*Kxy).sum() / (n*(n-1))
        mmd_stats[i] = mmd

    return mmd_stats
