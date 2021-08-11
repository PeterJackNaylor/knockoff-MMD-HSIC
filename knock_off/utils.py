
import numpy as np
from scipy.sparse.linalg import eigsh

def screen(X, y, d, tr):

    if len(y.shape) == 1:
        q = 1
    else:
        q = y.shape[1]
    Xy = np.concatenate([X, y], axis=0)

    def w_j(sample_xy):
        x, y = sample_xy[:-q], sample_xy[-q:]
        return tr(x, y)

    w_js = np.apply_along_axis(w_j, 1, Xy)

    return w_js.argsort()[-d:][::-1]




def build_knockoff(X, y, d, tr):
    newX = get_equi_features(X)
    def w_j(i):
        x_j = newX[:, i]
        x_j_hat = newX[:, i+d]
        return tr(x_j, y) - tr(x_j_hat, y)
    wjs = list(map(w_j, np.arrange(d)))
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
