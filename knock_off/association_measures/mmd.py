import numpy as np

from .kernel_tools import get_kernel_function


def MMD(X, Y, kernel='gaussian'):
    """ 
    V-statistic of MMD, to have the U- uncomment the np.fill_diagonal term
    """
    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1
    
    kernel, kernel_params = get_kernel_function(kernel, nfeats=d)

    Ky = kernel(Y[:, 0], **kernel_params)

    mmd_stats = np.zeros((d, 1))

    for i in range(d):
        Kx = kernel(X[:,i:i+1], **kernel_params)
        Kxy = kernel(X[:,i:i+1], Y, **kernel_params)

        mmd_matrix = Kx + Ky - Kxy - Kxy.T
        # np.fill_diagonal(mmd_matrix, 0)  # remove self-similarity terms
        # mmd = np.sum(mmd_matrix) / (n*(n-1))
        mmd_stats[i] = mmd_matrix.mean()
    return mmd_stats
