import numpy as np

from .kernel_tools import center, get_kernel_function


def HSIC(X, Y, kernel='gaussian', normalised=False, sigma=None):
    n, d = X.shape
    ny, dy = Y.shape

    assert n == ny
    assert dy == 1

    kernel, kernel_params = get_kernel_function(kernel, nfeats=sigma)

    Ky = center(kernel(Y[:, 0], **kernel_params))

    if normalised:
        hsic_yy = np.trace(np.matmul(Ky, Ky))

    hsic_stats = np.zeros((d, 1))
    for k in range(d):

        Kx = center(kernel(X[:,k:k+1], **kernel_params))
        hsic = np.trace(np.matmul(Kx, Ky))

        if normalised:
            hsic_xx = np.trace(np.matmul(Kx, Kx))
            norm = (hsic_xx * hsic_yy) ** 0.5
            hsic = hsic / norm

        hsic_stats[k] = hsic

    return hsic_stats
