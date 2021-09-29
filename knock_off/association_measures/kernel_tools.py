import numpy as np


def get_kernel_function(name, nfeats=1):
    if name == 'gaussian':
        kernel = kernel_gaussian
        if nfeats is not None:
            kernel_params = {'sigma': np.sqrt(nfeats)}
        else:
            kernel_params = {'sigma': None}
    elif name == "linear":
        kernel = kernel_linear
        kernel_params = {}
    elif name == "distance":
        kernel = kernel_alpha
        kernel_params = {'alpha': 1.}
    else:
        raise "No valid kernel."

    return kernel, kernel_params

def compute_distance_matrix(x1, x2=None):
    if len(x1.shape) == 1:
        x1 = np.expand_dims(x1, axis=1)

    x1_2 = np.power(x1, 2)

    if x2 is not None:
        if len(x2.shape) == 1:
            x2 = np.expand_dims(x2, axis=1)
        x2_2 = np.power(x2, 2)
    else:
        x2 = x1
        x2_2 = x1_2

    dist_2 = x2_2 + x1_2.T - 2 * np.dot(x2, x1.T)
    return dist_2

def kernel_gaussian(x1, x2=None, sigma=None):

    dist_2 = compute_distance_matrix(x1, x2)
    if sigma is None:
        sigma = 0.5 * np.sqrt(np.var(dist_2))
    K = np.exp(- 0.5 * dist_2 / sigma)

    return K

def kernel_linear(x1, x2=None):

    if len(x1.shape) == 1:
        x1 = np.expand_dims(x1, axis=1)

    if x2 is not None:
        if len(x2.shape) == 1:
            x2 = np.expand_dims(x2, axis=1)
    else:
        x2 = x1

    result = np.dot(x2, x1.T)
    return result

def kernel_alpha(x1, x2=None, alpha=None):
    if len(x1.shape) == 1:
        x1 = np.expand_dims(x1, axis=1)
    x1_alpha = np.power(np.abs(x1), alpha)

    if x2 is not None:
        if len(x2.shape) == 1:
            x2 = np.expand_dims(x2, axis=1)
        x2_alpha = np.power(np.abs(x2), alpha)
    else:
        x2 = x1
        x2_alpha = x1_alpha

    result = 0.5 * (x1_alpha + x2_alpha.T - np.power(np.abs(x2.T - x1), alpha))
    return result
    
def center(K):

    n, d = K.shape

    assert n == d

    H = np.eye(n) - 1 / n * np.ones((n, n))
    KH = np.matmul(K, H)

    return KH
