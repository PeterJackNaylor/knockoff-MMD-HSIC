import numpy as np

from .kernel_tools import get_kernel_function, compute_distance_matrix


def calibrate_sigma_mmd(x):
    """
    Calibrates sigma for the gaussian kernel as the median
    distance of elements of X.
    Parameters
    ----------
    X : numpy array like object where the rows correspond to the samples
        and the columns to features.

    Returns
    -------
    Scalar sigma
    """
    result = np.median(compute_distance_matrix(x.flatten()))
    return 0.5 * result


def indexes_with_respect_to_y(Y):
    """
    Checks Y and returns indexes with respect to the groups.
    Parameters
    ----------
    Y : numpy array like of one single output.
        Corresponding to a categorical variable.
    Returns
    -------
    List of indexes corresponding to each group.
    """
    categories = np.unique(Y)
    n_c = categories.shape[0]
    assert n_c >= 2
    indexes = []

    for cat in list(categories):
        i_index = np.where(Y == cat)[0]
        indexes.append(i_index)

    return indexes


def cMMD(X, Y, kernel="gaussian", sigma=None):
    """
    Computes the cMMM between X and Y with a given kernel.
    Parameters
    ----------
    X : numpy array like object where the rows correspond to the samples
        and the columns to features.

    Y : numpy array like, of same size as X and one single output.
        Corresponding to a categorical variable.

    kernel: string designating or distance, gaussian or linear


    sigma: None or float, hyper parameter for the gaussian kernel.
        If set to None, it takes sigma as the median of distance matrix.

    Returns
    -------
    numpy array of size the number of input features of X
    which holds the MMD between each feature and Y.
    """
    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1

    indexes = indexes_with_respect_to_y(Y)

    mmd_stats = np.zeros((d, 1))
    for k in range(d):
        mmd_stats[k] = cMMD_index(
            X[:, k],
            group_idx=indexes,
            kernel_name=kernel,
            sigma=sigma,
        )

    return mmd_stats


def cMMD_index(X, group_idx, kernel_name="gaussian", sigma=None):
    """
    General cMMD V-statistic to be used zith X and categorical data.
    Implements the formula given by
    *Expected Conditional Characteristic Function-based Measures for Testing
    Independence* by Ke et Al 2020.
    Parameters
    ----------
    X : numpy array like object where the rows correspond to the samples
        and the columns to features.

    group_idx : numpy array like, of same size as X containing the group
        information.

    kernel_name: string designating or distance, gaussian or linear

    sigma: None or float, hyper parameter for the gaussian kernel.
        If set to None, it takes sigma as the median of distance matrix.

    Returns
    -------
    numpy array of size the number of input features of X
    which holds the cMMD with respect to the groups.
    """
    n = sum([len(el) for el in group_idx])
    number_of_groups = len(group_idx)
    assert number_of_groups > 1
    assert n == X.shape[0]

    kernel, kernel_params = get_kernel_function(kernel_name, nfeats=sigma)

    if sigma is None and kernel_name == "gaussian":
        sigma = calibrate_sigma_mmd(X)
        kernel_params["sigma"] = sigma

    group_estimates = np.zeros(number_of_groups)
    for i, grp in enumerate(group_idx):
        n_group = grp.shape[0]
        Kx_group = kernel(X[grp], **kernel_params)
        group_estimates[i] = Kx_group.sum() / n_group

    Kx = kernel(X, **kernel_params)

    mmd_matrix = group_estimates.sum() / n - Kx.sum() / (n ** 2)

    return mmd_matrix
