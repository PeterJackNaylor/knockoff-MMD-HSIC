import numpy as np

from .kernel_tools import get_kernel_function, compute_distance_matrix

def calibrate_sigma_mmd(x):
    result = np.median(compute_distance_matrix(x.flatten()))
    return 0.5 * result

def indexes_with_respect_to_y(Y):

    categories = np.unique(Y)
    n_c = categories.shape[0]
    assert n_c >= 2
    indexes = []

    for cat in list(categories):
        i_index = np.where(Y == cat)[0]
        indexes.append(i_index)
    
    return indexes

def MMD(X, Y, kernel='gaussian', normalised=False, sigma=None):
    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1

    indexes = indexes_with_respect_to_y(Y)

    mmd_stats = np.zeros((d, 1))
    for k in range(d):
        mmd_stats[k] = MMD_index(
            X[:,k],
            group_idx=indexes,
            kernel_name=kernel,
            normalised=normalised,
            sigma=sigma)
    
    return mmd_stats

def MMD_index(X, group_idx, kernel_name='gaussian', normalised=False, sigma=None):
    """
    General MMD V-statistic to be used for specific cases. X and Y correspond
    to two distribution with the same domain.
    """
    n = sum([len(el) for el in group_idx])
    number_of_groups = len(group_idx)
    assert number_of_groups > 1
    assert n == X.shape[0]

    kernel, kernel_params = get_kernel_function(kernel_name, nfeats=sigma)

    if sigma is None and kernel_name == "gaussian":
        sigma = calibrate_sigma_mmd(X)
        kernel_params['sigma'] = sigma
    
    group_estimates = np.zeros(number_of_groups)
    for i, grp in enumerate(group_idx):
        n_group = grp.shape[0]
        Kx_group =  kernel(X[grp], **kernel_params)
        group_estimates[i] = Kx_group.sum() / n_group

    Kx = kernel(X, **kernel_params)

    mmd_matrix = group_estimates.sum() / n - Kx.sum() / (n ** 2)

    if normalised:
        norm = np.trace(Kx) / n - Kx.sum() / (n**2)  
        mmd_matrix = mmd_matrix / norm
    
    # np.fill_diagonal(mmd_matrix, 0)  # remove self-similarity terms
    # mmd = np.sum(mmd_matrix) / (n*(n-1))
    return mmd_matrix
