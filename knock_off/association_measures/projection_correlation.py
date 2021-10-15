import numpy as np


def get_arccos(X):
    """
    Computes the arccos of X as defined in *Model-Free Feature
    Screening and FDR Control With Knockoff Features*
    by Liu et Al (2020).
    Code taken from https://github.com/TwoLittle/PC_Screen
    Parameters
    ----------
    X : numpy array like object with one column where the
        rows correspond to the samples.
    Returns
    -------
    A scalar arccos of X
    """
    # X is a 2-d array

    n, p = X.shape
    cos_a = np.zeros([n, n, n])

    for r in range(n):

        xr = X[r]
        X_r = (X - xr).astype(float)  # dealing with categorical values
        cross = np.dot(X_r, X_r.T)
        row_norm = np.sqrt(np.sum(X_r ** 2, axis=1))

        outer_norm = np.outer(row_norm, row_norm)

        zero_idx = outer_norm == 0.0
        outer_norm[zero_idx] = 1.0
        cos_a_kl = cross / outer_norm
        cos_a_kl[zero_idx] = 0.0

        cos_a[:, :, r] = cos_a_kl

    cos_a[cos_a > 1] = 1.0
    cos_a[cos_a < -1] = -1.0
    a = np.arccos(cos_a)

    a_bar_12 = np.mean(a, axis=0, keepdims=True)
    a_bar_02 = np.mean(a, axis=1, keepdims=True)
    a_bar_2 = np.mean(a, axis=(0, 1), keepdims=True)
    A = a - a_bar_12 - a_bar_02 + a_bar_2

    return a, A


def projection_corr(X, Y):
    """
    Computes the Projection Correlation between X and Y as defined
    by *Model-Free Feature Screening and FDR Control
    With Knockoff Features* by Liu et Al (2020).
    Code taken from https://github.com/TwoLittle/PC_Screen
    Parameters
    ----------
    X : numpy array like object where the rows correspond to the samples
        and the columns to features.

    Y : numpy array like, of same size as X and one single output.

    Returns
    -------
    numpy array of size the number of input features of X
    which holds the Projection Correlation between
    each feature and Y.
    """
    # In original code
    # X = np.expand_dims(X, axis=1)
    # Y = np.expand_dims(Y, axis=1)

    # X, Y are 2-d array
    nx, p = X.shape
    ny, q = Y.shape
    assert q == 1
    assert nx == ny

    pr_stats = np.zeros((p, 1))

    for i in range(p):
        a_x, A_x = get_arccos(X[:, i:(i+1)])
        a_y, A_y = get_arccos(Y[:, 0:1])

        S_xy = np.sum(A_x * A_y) / (nx ** 3)
        S_xx = np.sum(A_x ** 2) / (nx ** 3)
        S_yy = np.sum(A_y ** 2) / (nx ** 3)

        if S_xx * S_yy == 0.0:
            corr = 0.0
        else:
            corr = np.sqrt(S_xy / np.sqrt(S_xx * S_yy))
        pr_stats[i] = corr
    return pr_stats
