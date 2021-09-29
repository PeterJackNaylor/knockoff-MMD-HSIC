import numpy as np

from .kernel_tools import center, get_kernel_function

def HSIC_linear(X, Y, kernel='linear', sigma=None):

    return HSIC_v(X, Y, 
        kernel=kernel,
        input_norm=False,
        normed=False,
        sigma=sigma)

def HSIC_linear_norm(X, Y, kernel='linear', sigma=None):

    return HSIC_v(X, Y, 
        kernel=kernel,
        input_norm=False,
        normed=True,
        sigma=sigma)

def HSIC_distance(X, Y, kernel='distance', sigma=None):

    return HSIC_v(X, Y, 
        kernel=kernel,
        input_norm=False,
        normed=False,
        sigma=sigma)

def HSIC_distance_norm(X, Y, kernel='distance', sigma=None):

    return HSIC_v(X, Y, 
        kernel=kernel,
        input_norm=False,
        normed=True,
        sigma=sigma)

def HSIC_rbf(X, Y, kernel='gaussian', sigma=None):

    return HSIC_v(X, Y, 
        kernel=kernel,
        input_norm=False,
        normed=False,
        sigma=sigma)

def HSIC_rbf_norm(X, Y, kernel='gaussian', sigma=None):

    return HSIC_v(X, Y, 
        kernel=kernel,
        input_norm=False,
        normed=True,
        sigma=sigma)

def HSIC_v(X, Y, kernel='gaussian', input_norm=False, normed=False, sigma=None):
    n, d = X.shape
    ny, dy = Y.shape

    assert n == ny
    assert dy == 1

    if input_norm:
        Y = Y / np.linalg.norm(Y)
    
    kernel, kernel_params = get_kernel_function(kernel, nfeats=sigma)

    Ky = center(kernel(Y[:, 0], **kernel_params))

    if normed:
        hsic_yy = np.trace(np.matmul(Ky, Ky))

    hsic_stats = np.zeros((d, 1))
    for k in range(d):

        if input_norm:
            X_tmp = X[:,k:k+1] / np.linalg.norm(X[:,k:k+1])
        else:
            X_tmp = X[:,k:k+1]

        Kx = center(kernel(X_tmp, **kernel_params))
        hsic = np.trace(np.matmul(Kx, Ky))

        if normed:
            hsic_xx = np.trace(np.matmul(Kx, Kx))
            norm = (hsic_xx * hsic_yy) ** 0.5
            hsic = hsic / norm

        hsic_stats[k] = hsic

    return hsic_stats
