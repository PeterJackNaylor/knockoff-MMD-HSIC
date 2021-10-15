import numpy as np

from .kernel_tools import center, get_kernel_function


def HSIC(X, Y, kernel="gaussian", normalised=False, sigma=None):
    """
    Computes the HSIC between X and Y with a given kernel
    Parameters
    ----------
    X : numpy array like object where the rows correspond to the samples
        and the columns to features.

    Y : numpy array like, of same size as X and one single output.

    kernel: string designating or distance, gaussian or linear

    normalised: bool, wether or not to use the normalised HSIC
        where HSICn = HSIC(X, Y) / (HSIC(X,X).HSIC(Y,Y)) **0.5

    sigma: None or float, hyper parameter for the gaussian kernel.
        If set to None, it takes sigma as the median of distance matrix.

    Returns
    -------
    numpy array of size the number of input features of X
    which holds the HSIC between each feature and Y.
    """
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

        Kx = center(kernel(X[:, k:(k+1)], **kernel_params))
        hsic = np.trace(np.matmul(Kx, Ky))

        if normalised:
            hsic_xx = np.trace(np.matmul(Kx, Kx))
            norm = (hsic_xx * hsic_yy) ** 0.5
            hsic = hsic / norm

        hsic_stats[k] = hsic

    return hsic_stats
