import numpy as np
from scipy.stats import pearsonr


def pearson_correlation(X, Y):
    """
    Computes the absolute pearson correlation between X and Y.
    Parameters
    ----------
    X : numpy array like object where the rows correspond to the samples
        and the columns to features.

    Y : numpy array like, of same size as X and one single output.

    Returns
    -------
    numpy array of size the number of input features of X
    which holds the absolute pearson correlation between
    each feature and Y.
    """
    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1
    pearson_stats = np.zeros((d, 1))
    for i in range(d):
        try:
            pearson_stats[i] = np.array(
                [np.float32(abs(pearsonr(X[:, i], Y[:, 0])[0]))]
            )
        except:
            pearson_stats[i] = float("nan")

    return pearson_stats
