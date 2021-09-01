import numpy as np

from knock_off.association_measures import distance_corr, projection_corr, tr, HSIC, MMD
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

x = np.array([35, 23, 47, 17, 10, 43, 9, 6, 28]).reshape(9, 1)
y = np.array([30, 33, 45, 23, 8, 49, 12, 4, 31]).reshape(9, 1)

def test_distance_correlation():
    # sanity check
    stats = distance_corr(X, Y)
    assert len(stats) == X.shape[1]

    # checked with https://rdrr.io/cran/Rfast/
    dc_ = distance_corr(x, y)
    ans = 0.9513721
    np.testing.assert_almost_equal(dc_, ans)
    
def test_projection_correlation():
    # sanity check
    stats = projection_corr(X, Y)
    assert len(stats) == X.shape[1]

    ## TODO This one has not been checked.
    pc_ = projection_corr(x, y)
    ans = 0.65911018 
    np.testing.assert_almost_equal(pc_, ans)

def test_tr_measure():
    # sanity check
    stats = tr(X, Y)
    assert len(stats) == X.shape[1]

    # 3 * tau - 2 * rho
    # rho = 0.9
    # tau = 26 / 36
    # => tr = 0.36666666
    tr_ = tr(x, y)
    ans = 3 * 26 / 36 - 2 * 0.9
    np.testing.assert_almost_equal(tr_, ans)


def test_hsic():
    hsic = HSIC(X, Y)

    ref = np.zeros((50, 1))
    for i in range(50):
        ref[i] = ref_hsic(X[:,i].reshape(10,1), Y, 50)

    assert len(hsic) == X.shape[1]
    assert all(hsic >= 0)
    assert np.all(ref - hsic < 10e-20)

    ## TODO this one has not been checked
    # I got 0.09954543 with another method..
    hsic_ = HSIC(x, y)
    ans = 0.01137139
    np.testing.assert_almost_equal(hsic_, ans)

    x_2 = np.random.rand(10, 1)
    assert np.all(HSIC(x_2, x_2**2) > hsic)

def test_mmd():
    mmd = MMD(X, Y)

    assert len(mmd) == X.shape[1]
    # assert all(mmd >= 0)


    ## tested against https://github.com/AnthonyEbert/EasyMMD
    ## MMD(x, y) gave -0.03217994 with the R package
    mmd_ = MMD(x, y)
    ans = -0.01159811
    np.testing.assert_almost_equal(mmd_, ans)


    x_2 = np.random.rand(10, 1)
    assert np.all(MMD(x_2, x_2**2) > mmd)



