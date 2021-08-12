from .kernel_tools import *


def HSIC(X, Y, kernel=kernel_gaussian):

    n, d = X.shape
    sigma = np.sqrt(d)
    ny = len(Y)

    assert n == ny

    Ky = kernel(Y, sigma)
    Ky = center_K(Ky)

    hsic_stats = []

    for x in X.T:
        Kx = kernel(x, sigma)
        Kx = center_K(Kx)
        hsic = np.trace(np.dot(Kx.T, Ky))
        hsic_stats.append(hsic)

    return hsic_stats
