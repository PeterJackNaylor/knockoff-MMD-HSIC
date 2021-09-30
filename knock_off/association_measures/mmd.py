import numpy as np

from .kernel_tools import get_kernel_function, compute_distance_matrix

def calibrate_sigma_mmd(x, y):
    flat = np.concatenate([x.flatten(), y.flatten()], axis=0)
    result = np.median(compute_distance_matrix(flat))
    return 0.5 * result

def split_x_with_respect_to_y(X, Y):

    categories = np.unique(Y)
    assert categories.shape[0] == 2

    Y0_idx = np.where(Y == categories[0])[0]
    Y1_idx = np.where(Y == categories[1])[0]

    n0 = Y0_idx.shape[0]
    n1 = Y1_idx.shape[0]

    if n0 > n1:
        Y0_idx = np.random.choice(Y0_idx, size=n1, replace=False)
    elif n0 < n1:
        Y1_idx = np.random.choice(Y1_idx, size=n0, replace=False)
    
    X0 = X[Y0_idx,]
    X1 = X[Y1_idx,]

    return X0, X1

def MMD(X, Y, kernel='gaussian', normalised=False, sigma=None):
    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1

    X0, X1 = split_x_with_respect_to_y(X, Y)

    mmd_stats = np.zeros((d, 1))

    for k in range(d):
        mmd_stats[k] = MMD_v(
            X0[:,k], X1[:,k],
            kernel=kernel,
            normalised=normalised,
            sigma=sigma)
    
    return mmd_stats

def MMD_v(X, Y, kernel='gaussian', normalised=False, sigma=None):
    """
    General MMD V-statistic to be used for specific cases. X and Y correspond
    to two distribution with the same domain.
    """
    n = X.shape[0]
    
    kernel, kernel_params = get_kernel_function(kernel, nfeats=sigma)

    if sigma is None and kernel == "gaussian":
        sigma = calibrate_sigma_mmd(X, Y)
        kernel_params['sigma'] = sigma
    
    Ky = kernel(Y, **kernel_params)
    Kx = kernel(X, **kernel_params)
    Kxy = kernel(X, Y, **kernel_params)

    mmd_matrix = (Kx + Ky - Kxy - Kxy.T).mean()

    if normalised:
        norm = np.trace(Kx) / n - Kx.sum() / (n**2)  
        mmd_matrix = mmd_matrix / norm
    
    # np.fill_diagonal(mmd_matrix, 0)  # remove self-similarity terms
    # mmd = np.sum(mmd_matrix) / (n*(n-1))
    return mmd_matrix
