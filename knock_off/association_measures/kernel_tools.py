import numpy as np


def get_kernel_function(name, nfeats=1):
    """
    Get the correct kernel function given the name.
    For the gaussian kernel nfeats designates sigma.
    Parameters
    ----------
    name: string, could be gaussian, linear or distance.

    nfeats: None or scalar, if None, it is set as the median
        of the distance matrix of the input, otherwise it is
        set as sqrt(nfeats)

    Returns
    -------
    A tuple, where the first element is the kernel function
    and the second it's hyper parameter dictionnary.
    """
    if name == "gaussian":
        kernel = kernel_gaussian
        if nfeats is not None:
            kernel_params = {"sigma": np.sqrt(nfeats)}
        else:
            kernel_params = {"sigma": None}
    elif name == "linear":
        kernel = kernel_linear
        kernel_params = {}
    elif name == "distance":
        kernel = kernel_alpha
        kernel_params = {"alpha": 1.0}
    else:
        raise "No valid kernel."

    return kernel, kernel_params


def compute_distance_matrix(x1, x2=None):
    """
    Computes the distance matrix between x1 and x2.
    If x2 isn't given, it will set x2 as x1 and compute
    the inner distance matrix of x1.
    Parameters
    ----------
    x1: numpy array like object with one feature where the rows
        designate samples.

    x2: None or like x1.

    Returns
    -------
    The distance matrix of x1 and x2.
    """
    x1 = check_vector(x1)
    x1_2 = np.power(x1, 2)

    x2 = x1 if x2 is None else check_vector(x2)
    x2_2 = np.power(x2, 2)

    dist_2 = x2_2 + x1_2.T - 2 * np.dot(x2, x1.T)
    return dist_2


def kernel_gaussian(x1, x2=None, sigma=None):
    """
    Computes the distance matrix with the gaussian kernel.
    If x2 isn't given, it will set x2 as x1 and compute
    the inner distance matrix of x1.
    If sigma is not given, it will be set according to the
    median of the distance matrix.
    Parameters
    ----------
    x1: numpy array like object with one feature where the rows
        designate samples.

    x2: None or like x1.

    sigma: None or float, hyper parameter for the gaussian kernel.
        If set to None, it takes sigma as the median of distance matrix.

    Returns
    -------
    The gaussian kernel of the distance matrix of x1 and x2.
    """
    dist_2 = compute_distance_matrix(x1, x2)
    if sigma is None:
        sigma = 0.5 * np.sqrt(np.var(dist_2))
    K = np.exp(-0.5 * dist_2 / sigma)

    return K


def kernel_linear(x1, x2=None):
    """
    Computes the distance matrix with the linear kernel.
    If x2 isn't given, it will set x2 as x1 and compute
    the inner distance matrix of x1.
    Parameters
    ----------
    x1: numpy array like object with one feature where the rows
        designate samples.

    x2: None or like x1.

    Returns
    -------
    The linear kernel of the distance matrix of x1 and x2.
    """
    x1 = check_vector(x1)
    x2 = x1 if x2 is None else check_vector(x2)

    result = np.dot(x2, x1.T)
    return result


def kernel_alpha(x1, x2=None, alpha=None):
    """
    Computes the distance matrix with the distance alpha kernel.
    If x2 isn't given, it will set x2 as x1 and compute
    the inner distance matrix of x1.
    If alpha isn't set, it's default value is 1.
    Parameters
    ----------
    x1: numpy array like object with one feature where the rows
        designate samples.

    x2: None or like x1.

    sigma: None or float, hyper parameter for the distance alpha kernel.
        If set to None, it takes the value of 1.

    Returns
    -------
    The distance alpha kernel of the distance matrix of x1 and x2.
    """
    x1 = check_vector(x1)
    x1_alpha = np.power(np.abs(x1), alpha)

    x2 = x1 if x2 is None else check_vector(x2)
    x2_alpha = np.power(np.abs(x2), alpha)

    result = 0.5 * (x1_alpha + x2_alpha.T - np.power(np.abs(x2.T - x1), alpha))
    return result


def check_vector(x):
    """
    Checks wether the numpy array x needs to be expended
    to contain a second dimension.
    Parameters
    ----------
    x:  numpy array like object with one feature where the rows
        designate samples.
    Returns
    -------
    The same vector x with an extra dimension if it didn't originally
    have one.
    """
    if len(x.shape) == 1:
        x = np.expand_dims(x, axis=1)

    return x


def center(K):
    """
    Matrix centering
    Parameters
    ----------
    x:  square numpy array like object
    Returns
    -------
    The centered matrix.
    """
    n, d = K.shape

    assert n == d

    H = np.eye(n) - 1 / n * np.ones((n, n))
    KH = np.matmul(K, H)

    return KH
