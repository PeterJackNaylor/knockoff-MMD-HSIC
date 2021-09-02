import numpy as np

from knock_off.association_measures.hsic import HSIC
from knock_off.association_measures.mmd import MMD
from knock_off.association_measures.kernel_tools import get_kernel_function

np.random.seed(42)
X = np.random.randn(10, 50)
Y = np.random.randn(10, 1)

# reference implementation from https://github.com/jenninglim/multiscale-features/blob/master/mskernel/hsic.py
def ref_hsic(X, Y, d):
    """
    From: https://github.com/wittawatj/fsic-test/blob/master/fsic/indtest.py
    Compute the biased estimator of HSIC as in Gretton et al., 2005.
    :param k: a Kernel on X
    :param l: a Kernel on Y
    """
    if X.shape[0] != Y.shape[0]:
        raise ValueError('X and Y must have the same number of rows (sample size')

    n = X.shape[0]

    kernel, kernel_params = get_kernel_function('gaussian', nfeats=d)

    K = kernel(X, **kernel_params)
    L = kernel(Y, **kernel_params)
    Kmean = np.mean(K, 0)
    Lmean = np.mean(L, 0)
    HK = K - Kmean
    HL = L - Lmean
    # t = trace(KHLH)
    HKf = HK.flatten()/(n)
    HLf = HL.T.flatten()/(n)
    hsic = HKf.dot(HLf)

    return hsic


def test_hsic():
    hsic = HSIC(X, Y)

    ref = np.zeros((50, 1))
    for i in range(50):
        ref[i] = ref_hsic(X[:,i].reshape(10,1), Y, 50)

    assert len(hsic) == X.shape[1]
    assert all(hsic>= 0)
    assert np.all(ref - hsic < 10e-20)

    x = np.random.rand(10, 1)
    assert np.all(HSIC(x, x**2) > hsic)


def test_mmd():
    mmd = MMD(X, Y)

    assert len(mmd) == X.shape[1]
    assert all(mmd >= 0)

    x = np.random.rand(10, 1)
    assert np.all(MMD(x, x**2) > mmd)
