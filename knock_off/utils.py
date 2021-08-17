
import numpy as np
from scipy.sparse.linalg import eigsh

def screen(X, y, d, am):
    
    def w_j(x_j):
        return am(x_j, y)

    w_js = np.apply_along_axis(w_j, 0, X)
    return w_js.argsort()[-d:][::-1]




def build_knockoff(X, y, am):
    d = X.shape[1]
    X_hat = get_equi_features(X)
    def w_j(i):
        x_j = X[:, i]
        x_j_hat = X_hat[:, i]
        return am(x_j, y) - am(x_j_hat, y)
    wjs = list(map(w_j, np.arange(d)))
    return wjs


def orthonormalize(X):
    # X is a 2-d array
    # output: Gram-Schmidt orthogonalization of X
    
    n, p = X.shape
    Y = np.zeros([n, p])
    Y[:, 0] = X[:, 0] / np.sqrt(np.sum(X[:, 0]**2))
    
    for j in range(1, p):
        
        Yj = Y[:, range(j)]
        xj = X[:, j]
        w = np.dot(xj, Yj)
        xj_p = np.sum(w*Yj, axis = 1)
        yj = xj - xj_p
        yj = yj / np.sqrt(np.sum(yj**2))
        
        Y[:, j] = yj
        
    return Y


def get_equi_features(X):
    # X is 2-d array

    n, p = X.shape
    scale = np.sqrt(np.sum(X**2, axis=0))
    Xstd = X / scale
    sigma = np.dot(Xstd.T, Xstd)
    sigma_inv = np.linalg.inv(sigma)
    lambd_min = eigsh(sigma, k=1, which='SA')[0].squeeze()
    sj = np.min([1., 2.*lambd_min])
    sj = sj - 0.00001

    mat_s = np.diag([sj]*p)
    A = 2*mat_s - sj*sj*sigma_inv
    C = np.linalg.cholesky(A).T

    Xn = np.random.randn(n, p)
    XX = np.hstack([Xstd, Xn])
    XXo = orthonormalize(XX)

    U = XXo[:, range(p,2*p)]
    
    Xnew = np.dot(Xstd, np.eye(p) - sigma_inv * sj) + np.dot(U, C)
    return Xnew



def knock_off_check_parameters(n, p, n1, d):
    set_one, set_two = None, None
    screening, stop = False, False
    msg = ''

    if n in [1, 2, 3]:
        # not possible because we want d < n / 2
        msg = "Fit is not possible, data too small and \
can't satisfy condition d < n_2 / 2"
        index = list(np.arange(p))
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
            d = n2 / 2 - 1
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
    
    return stop, screening, set_one, set_two, msg