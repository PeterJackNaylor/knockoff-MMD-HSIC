import numpy as np

from .kernel_tools import get_kernel_function, compute_distance_matrix

def calibrate_sigma_mmd(x, y):
    flat = np.concatenate([x.flatten(), y.flatten()], axis=0)
    return np.median(compute_distance_matrix(flat))

# def MMD(X, Y, kernel='gaussian', sigma=0.01):
#     """ 
#     V-statistic of MMD, to have the U- uncomment the np.fill_diagonal term
#     """
#     n, d = X.shape
#     ny, nd = Y.shape

#     assert n == ny
#     assert nd == 1
#     Y = Y / np.linalg.norm(Y)
    
    
#     kernel, kernel_params = get_kernel_function(kernel, nfeats=sigma)

#     Ky = kernel(Y[:, 0], **kernel_params)

#     mmd_stats = np.zeros((d, 1))

#     for k in range(d):
#         X_norm = X[:,k:k+1] / np.linalg.norm(X[:,k:k+1])
#         kernel_params['sigma'] = calibrate_sigma_mmd(X_norm, Y)
#         Kx = kernel(X_norm, **kernel_params)
#         Kxy = kernel(X_norm, Y, **kernel_params)

#         mmd_matrix = Kx + Ky - Kxy - Kxy.T
#         # np.fill_diagonal(mmd_matrix, 0)  # remove self-similarity terms
#         # mmd = np.sum(mmd_matrix) / (n*(n-1))
#         mmd_stats[k] = mmd_matrix.mean()
#     return mmd_stats

def MMD(X, Y, kernel='gaussian', sigma=None):
    """ 
    V-statistic of MMD normalised.
    X is the input and Y the labels.
    Y has to be a binary vector.
    """
    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1

    categories = np.unique(Y)
    assert categories.shape[0] == 2

    Y0_idx = np.where(Y == categories[0])[0]
    Y1_idx = np.array(list(set(np.arange(n)) - set(Y0_idx)))

    n0 = Y0_idx.shape[0]
    n1 = Y1_idx.shape[0]

    if n0 > n1:
        Y0_idx = np.random.choice(Y0_idx, size=n1, replace=False)
    elif n0 < n1:
        Y1_idx = np.random.choice(Y1_idx, size=n0, replace=False)
    
    X0 = X[Y0_idx,]
    X1 = X[Y1_idx,]

    mmd_stats = np.zeros((d, 1))
    for k in range(d):
        mmd_stats[k] = MMD_v(
            X0[:,k:k+1], X1[:,k:k+1],
            kernel='gaussian',
            input_norm=True,
            normed=False,
            sigma=sigma)[0,0]
    
    return mmd_stats

def MMD_norm(X, Y, kernel='gaussian', sigma=None):
    """ 
    V-statistic of MMD normalised.
    X is the input and Y the labels.
    Y has to be a binary vector.
    """
    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1

    categories = np.unique(Y)
    assert categories.shape[0] == 2

    Y0_idx = np.where(Y == categories[0])
    Y1_idx = np.array(set(np.arange(n)) - set(Y0_idx))

    n0 = Y0_idx.shape[0]
    n1 = Y1_idx.shape[0]

    if n0 > n1:
        Y0_idx = np.random.choice(Y0_idx, size=n1, replace=False)
    elif n0 < n1:
        Y1_idx = np.random.choice(Y1_idx, size=n0, replace=False)
    
    X0 = X[Y0_idx,]
    X1 = X[Y1_idx,]

    mmd_stats = np.zeros((d, 1))
    
    for k in range(d):
        mmd_stats[k] = MMD_v(
            X0[:,k:k+1], X1[:,k:k+1],
            kernel='gaussian',
            input_norm=True,
            normed=True,
            sigma=sigma)[0,0]
    return mmd_stats


def MMD_v(X, Y, kernel='gaussian', input_norm=True, normed=False, sigma=None):
    """
    General MMD V-statistic to be used for specific cases. X and Y correspond
    to two distribution with the same domain.
    """

    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1

    if input_norm:
        Y = Y / np.linalg.norm(Y)
    
    if sigma is None:
        calibrate_sigma = True
        sigma = 1.
    else:
        calibrate_sigma = False
    
    kernel, kernel_params = get_kernel_function(kernel, nfeats=sigma)

    Ky = kernel(Y[:, 0], **kernel_params)

    mmd_stats = np.zeros((d, 1))

    for k in range(d):
        if input_norm:
            X_tmp = X[:,k:k+1] / np.linalg.norm(X[:,k:k+1])
        else:
            X_tmp = X[:,k:k+1]

        if calibrate_sigma:
            kernel_params['sigma'] = calibrate_sigma_mmd(X_tmp, Y)

        Kx = kernel(X_tmp, **kernel_params)
        Kxy = kernel(X_tmp, Y, **kernel_params)

        mmd_matrix = (Kx + Ky - Kxy - Kxy.T).mean()

        if normed:
            norm = np.trace(Kx) / n - Kx.sum() / (n**2)  
            mmd_matrix = mmd_matrix / norm
        # np.fill_diagonal(mmd_matrix, 0)  # remove self-similarity terms
        # mmd = np.sum(mmd_matrix) / (n*(n-1))
        mmd_stats[k] = mmd_matrix
    return mmd_stats
