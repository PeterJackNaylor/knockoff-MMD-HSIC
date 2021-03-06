import numpy as np

from knock_off.association_measures import (
    distance_corr, projection_corr, tr, HSIC, cMMD
)
from knock_off.association_measures.kernel_tools import get_kernel_function

np.random.seed(42)
X = np.random.randn(10, 50)
Y = np.random.randn(10, 1)
Y_c = np.random.randint(0, 2, size=10)

x = np.array([35, 23, 47, 17, 10, 43, 9, 6, 28]).reshape(9, 1)
y = np.array([30, 33, 45, 23, 8, 49, 12, 4, 31]).reshape(9, 1)
y_c = np.array([0, 0, 0, 1, 1, 0, 1, 1, 0]).reshape(9, 1)

# reference implementation from
# https://github.com/jenninglim/multiscale-features/blob/master/mskernel/hsic.py


def ref_hsic(X, Y, kernel, sigma):
    """
    From: https://github.com/wittawatj/fsic-test/blob/master/fsic/indtest.py
    Compute the biased estimator of HSIC as in Gretton et al., 2005.
    :param k: a Kernel on X
    :param l: a Kernel on Y
    """

    if X.shape[0] != Y.shape[0]:
        msg = "X and Y must have the same number of rows (sample size)"
        raise ValueError(msg)

    n = X.shape[0]

    kernel, kernel_params = get_kernel_function(kernel, nfeats=sigma)

    K = kernel(X, **kernel_params)
    L = kernel(Y, **kernel_params)
    Kmean = np.mean(K, 0)
    Lmean = np.mean(L, 0)
    HK = K - Kmean
    HL = L - Lmean
    # t = trace(KHLH)
    HKf = HK.flatten() / (n)
    HLf = HL.T.flatten() / (n)
    hsic = HKf.dot(HLf)

    return hsic


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
    hsic = HSIC(X, Y, kernel="gaussian", sigma=50) / X.shape[0] ** 2

    ref = np.zeros((50, 1))
    for i in range(50):
        ref[i] = ref_hsic(
            X[:, i].reshape(10, 1),
            Y, kernel="gaussian", sigma=50
        )

    assert len(hsic) == X.shape[1]
    assert all(hsic >= 0)

    np.testing.assert_almost_equal(ref, hsic)

    # I got 0.09954543 with a R method..
    hsic_ = HSIC(x, y, sigma=1) / x.shape[0] ** 2
    ans = 0.09528812
    np.testing.assert_almost_equal(ans, hsic_)

    x_2 = np.random.rand(10, 1)
    assert np.all(HSIC(x_2, x_2 ** 2) > hsic)


def test_cmmd():
    cmmd = cMMD(X, Y, kernel="gaussian", sigma=None)

    assert len(cmmd) == X.shape[1]
    assert all(cmmd >= 0)

    mmd_ = cMMD(x, y_c, kernel="gaussian", sigma=None)
    ans = 0.2819887
    np.testing.assert_almost_equal(mmd_, ans)

    x_2 = np.random.rand(10, 1)
    y_2 = np.random.randint(0, 2, size=(10, 1))
    assert np.all(cMMD(x_2 ** 2, y_2) > cMMD(x_2, y_2))


def test_kernelfunction():
    d = 50
    kernel, kernel_params = get_kernel_function("gaussian", nfeats=d)
    Ky = kernel(Y[:, 0].reshape(10, 1), **kernel_params)
    assert (Ky >= 0).all()
    assert (Ky <= 1).all()
    for i in range(d):
        Xi = X[:, i].reshape(10, 1)
        Kx = kernel(Xi, **kernel_params)
        Kxy = kernel(Xi, Y[:, 0].reshape(10, 1), **kernel_params)
        assert (Kx >= 0).all()
        assert (Kx <= 1).all()
        assert (Kxy >= 0).all()
        assert (Kxy <= 1).all()


def test_positive():
    am = [HSIC, tr, distance_corr, projection_corr]

    for _ in range(10):
        X = np.random.randn(10, 50)
        Y = np.random.randn(10, 1)
        Y_c = np.random.randint(0, 2, size=(10, 1))
        for m in am:
            if not np.all(m(X, Y) > 0):
                print(m)
                assert False
        assert np.all(cMMD(X, Y_c) > 0)
