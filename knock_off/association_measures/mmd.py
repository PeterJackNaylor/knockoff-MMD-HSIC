from .kernel_tools import *


def MMD(X, Y, kernel=kernel_gaussian):

    n, d = X.shape
    sigma = np.sqrt(d)
    ny = len(Y)

    assert n == ny

    Ky = kernel(Y, sigma)

    mmd_stats = []

    for x in X.T:
        Kx = kernel(x, sigma)

        Kxy = kernel(x, sigma, Y)
        # set diagonal to 0?
        mmd = (Kx + Ky - 2*Kxy).sum() / (n*(n-1))
        mmd_stats.append(mmd)

    return mmd_stats
