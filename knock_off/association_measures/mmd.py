import numpy as np

from .kernel_tools import get_kernel_function, compute_distance_matrix

def calibrate_sigma_mmd(x, y):
    flat = np.concatenate([x.flatten(), y.flatten()], axis=0)
    result = np.median(compute_distance_matrix(flat))
    return 0.5 * result

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


def MMD_linear(X, Y, kernel='linear', sigma=None):
    return MMD(X, Y, kernel=kernel, sigma=sigma)

def MMD_linear_norm(X, Y, kernel='linear', sigma=None):
    return MMD_norm(X, Y, kernel=kernel, sigma=sigma)

def MMD_distance(X, Y, kernel='distance', sigma=None):
    return MMD(X, Y, kernel=kernel, sigma=sigma)

def MMD_distance_norm(X, Y, kernel='distance', sigma=None):
    return MMD_norm(X, Y, kernel=kernel, sigma=sigma)

def MMD_rbf(X, Y, kernel='gaussian', sigma=None):
    return MMD(X, Y, kernel=kernel, sigma=sigma)

def MMD_rbf_norm(X, Y, kernel='gaussian', sigma=None):
    return MMD_norm(X, Y, kernel=kernel, sigma=sigma)

def MMD(X, Y, kernel='distance', sigma=None):
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
            kernel=kernel,
            input_norm=True,
            normed=False,
            sigma=sigma)
    
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
            kernel=kernel,
            input_norm=True,
            normed=True,
            sigma=sigma)
    return mmd_stats


def MMD_v(X, Y, kernel='gaussian', input_norm=True, normed=False, sigma=None):
    """
    General MMD V-statistic to be used for specific cases. X and Y correspond
    to two distribution with the same domain.
    """

    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert d == 1
    assert nd == 1

    
    kernel, kernel_params = get_kernel_function(kernel, nfeats=sigma)

    if input_norm:
        # import pdb; pdb.set_trace()
        scalar_norm = np.linalg.norm(np.concatenate([X[:,0], Y[:,0]], axis=0))
        X = X[:,0] / scalar_norm #np.linalg.norm(X[:,0]) #scalar_norm
        Y = Y[:,0] / scalar_norm #np.linalg.norm(Y[:,0]) #scalar_norm
    else:
        X = X[:,0]
        Y = Y[:,0]

    if sigma is None and kernel == "gaussian":
        sigma = calibrate_sigma_mmd(X, Y)
        kernel_params['sigma'] = sigma
    
    Ky = kernel(Y, **kernel_params)
    Kx = kernel(X, **kernel_params)
    Kxy = kernel(X, Y, **kernel_params)

    mmd_matrix = (Kx + Ky - Kxy - Kxy.T).mean()

    if normed:
        norm = np.trace(Kx) / n - Kx.sum() / (n**2)  
        mmd_matrix = mmd_matrix / norm
    # np.fill_diagonal(mmd_matrix, 0)  # remove self-similarity terms
    # mmd = np.sum(mmd_matrix) / (n*(n-1))
    return mmd_matrix
