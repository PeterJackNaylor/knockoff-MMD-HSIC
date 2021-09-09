import numpy as np
from sklearn import metrics

from knock_off.association_measures import distance_corr, projection_corr, tr, HSIC, MMD
from knock_off.association_measures.kernel_tools import get_kernel_function

np.random.seed(42)
X = np.random.randn(10, 50)
Y = np.random.randn(10, 1)

x = np.array([35, 23, 47, 17, 10, 43, 9, 6, 28]).reshape(9, 1)
y = np.array([30, 33, 45, 23, 8, 49, 12, 4, 31]).reshape(9, 1)

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

# reference implementation https://github.com/jenninglim/multiscale-features/blob/master/mskernel/mmd.py
def ref_mmd(X, Y, d):

    if X.shape[0] != Y.shape[0]:
        raise ValueError('X and Y must have the same number of rows (sample size')

    n = X.shape[0]

    gamma =  0.5 / d

    XX = metrics.pairwise.rbf_kernel(X, X, gamma)
    YY = metrics.pairwise.rbf_kernel(Y, Y, gamma)
    XY = metrics.pairwise.rbf_kernel(X, Y, gamma)
    # np.fill_diagonal(XX, 0)
    # np.fill_diagonal(YY, 0)
    # np.fill_diagonal(XY, 0)
    return (XX.mean() + YY.mean() - XY.mean() - XY.T.mean())



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

    np.testing.assert_almost_equal(ref, hsic)

    # I got 0.09954543 with a R method..
    hsic_ = HSIC(x, y)
    ans = 0.09528812
    np.testing.assert_almost_equal(ans, hsic_)

    x_2 = np.random.rand(10, 1)
    assert np.all(HSIC(x_2, x_2**2) > hsic)

def test_mmd():
    mmd = MMD(X, Y)

    ref = np.zeros((50, 1))
    for i in range(50):
        ref[i] = ref_mmd(X[:,i].reshape(10,1), Y, 50)

    assert len(mmd) == X.shape[1]
    assert all(mmd >= 0)
    np.testing.assert_almost_equal(ref, mmd)


    ## tested against https://github.com/AnthonyEbert/EasyMMD
    ## MMD(x, y) gave -0.03217994 with the R package , but that was U-stat
    ## this test is currently failing
    mmd_ = MMD(x, y)
    ans = 0.1858068
    np.testing.assert_almost_equal(mmd_, ans)


    x_2 = np.random.rand(10, 1)
    assert np.all(MMD(x_2, x_2**2) > mmd)



def test_kernelfunction():
    d = 50
    kernel, kernel_params = get_kernel_function('gaussian', nfeats=d)
    Ky = kernel(Y[:, 0].reshape(10,1), **kernel_params)
    assert (Ky >= 0).all()
    assert (Ky <= 1).all()
    for i in range(d):
        Kx = kernel(X[:, i].reshape(10,1), **kernel_params)
        Kxy = kernel(X[:, i].reshape(10,1), Y[:, 0].reshape(10,1), **kernel_params)
        assert (Kx >= 0).all()
        assert (Kx <= 1).all()
        assert (Kxy >= 0).all()
        assert (Kxy <= 1).all()
