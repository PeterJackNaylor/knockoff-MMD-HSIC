import numpy as np
from scipy.stats import kendalltau, spearmanr


def tr(X, Y):
    """
    Computes the absolute TR (Tau(Kendal) Rho(spearman)) between X and Y as
    defined by *Some newmeasures of dependence for random variables based
    on spearman’s rho and kendall tau* by  Lu et al.(2018).
    Parameters
    ----------
    X : numpy array like object where the rows correspond to the samples
        and the columns to features.

    Y : numpy array like, of same size as X and one single output.

    Returns
    -------
    numpy array of size the number of input features of X
    which holds the absolute TR between each feature and Y.
    """
    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1

    tr_stats = np.zeros((d, 1))

    for i in range(d):
        tau = kendalltau(X[:, i], Y[:, 0]).correlation
        rho = spearmanr(X[:, i], b=Y[:, 0]).correlation
        tr_stats[i] = abs(3 * tau - 2 * rho)

    return tr_stats


if __name__ == "__main__":
    x, y = [1, 2, 3, 4, 5], [5, 6, 7, 8, 7]
    print("rho: ", spearmanr(x, y).correlation)
    print("tau: ", kendalltau(x, y).correlation)
    print(f"{tr(x,y)=}")
