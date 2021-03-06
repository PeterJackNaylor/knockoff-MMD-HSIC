import numpy as np
from scipy.sparse.linalg import eigsh


def screen(X, y, d, am):
    """
    Returns the indices of the top d features and
    the unsorted list of scores on the features.
    """
    w_js = am(X, y)[:, 0]

    valid_features = w_js.shape[0] - np.sum(np.isnan(w_js))

    if valid_features < d:
        print(
            "the requested number of features ({}) could not be screened; \
only {} features were screened instead".format(
                d, valid_features
            )
        )
        d = valid_features

    # nans are at the end when sorting
    w_js[np.isnan(w_js)] = -float("inf")

    selected_indices = w_js.argsort()[-d:][::-1]
    return selected_indices, w_js


def build_knockoff(X, y, am, prescreened=None):
    """
    Builds knock off variables and uses if possible
    prescreened results.
    """
    if prescreened is None:
        X_wj = am(X, y)[:, 0]
    else:
        X_wj = prescreened

    X_hat = get_equi_features(X)
    X_hat_wj = am(X_hat, y)[:, 0]

    return X_wj - X_hat_wj


def orthonormalize(X):
    """
    Orthonomalizes X.
    Code taken from https://github.com/TwoLittle/PC_Screen
    """
    # X is a 2-d array
    # output: Gram-Schmidt orthogonalization of X

    n, p = X.shape
    Y = np.zeros([n, p])
    Y[:, 0] = X[:, 0] / np.sqrt(np.sum(X[:, 0] ** 2))

    for j in range(1, p):

        Yj = Y[:, range(j)]
        xj = X[:, j]
        w = np.dot(xj, Yj)
        xj_p = np.sum(w * Yj, axis=1)
        yj = xj - xj_p
        yj = yj / np.sqrt(np.sum(yj ** 2))

        Y[:, j] = yj

    return Y


def get_equi_features(X):
    """
    Builds the knockoff variables with the equicorrelated procedure.
    Code taken from https://github.com/TwoLittle/PC_Screen
    """
    # X is 2-d array
    n, p = X.shape
    scale = np.sqrt(np.sum(X ** 2, axis=0))
    Xstd = X / scale
    sigma = np.dot(Xstd.T, Xstd)
    sigma_inv = np.linalg.inv(sigma)
    lambd_min = eigsh(sigma, k=1, which="SA")[0].squeeze()
    sj = np.min([1.0, 2.0 * lambd_min])
    sj = sj - 0.00001

    mat_s = np.diag([sj] * p)
    A = 2 * mat_s - sj * sj * sigma_inv
    C = np.linalg.cholesky(A).T

    Xn = np.random.randn(n, p)
    XX = np.hstack([Xstd, Xn])
    XXo = orthonormalize(XX)

    U = XXo[:, range(p, 2 * p)]

    Xnew = np.dot(Xstd, np.eye(p) - sigma_inv * sj) + np.dot(U, C)
    return Xnew


def knock_off_check_parameters(n, p, n1, d):
    """
    Checks a variety of things with respect to n, p, n1 and d.
    Returns wether to perform screening.
    """
    set_one, set_two = None, None
    screening, stop = False, False
    msg = ""

    if n in [1, 2, 3]:
        # not possible because we want d < n / 2
        msg = "Fit is not possible, data too small and \
can't satisfy condition d < n_2 / 2"
        stop = True

    if p < n / 2:
        # we skip if we don't need to further reduce the number of features
        # in order to create exact knockoff features.
        screening = False
    else:
        n2 = n - int(n1 * n)
        # need to check
        if d >= n2 / 2:
            # d not set correctly so we set it to the highest plausible value
            d = int(n2 / 2 - 1)
            if d <= 0:
                msg = "Fit is not possible, data too small and \
can't satisfy condition d < n_2 / 2"
                stop = True
            else:
                msg = "d badly set, reseting"
        if not stop:
            screening = True
            msg = "Splitting the data"
            # split data
            indices = np.arange(n)
            np.random.shuffle(indices)
            set_one = indices[:int(n1 * n)]
            set_two = indices[int(n1 * n):]

    return stop, screening, set_one, set_two, d, msg
