import numpy as np

from knock_off.association_measures.hsic import HSIC
from knock_off.association_measures.mmd import MMD

X = np.random.randn(10, 50)
Y = np.random.randn(10, 1)


def test_hsic():
    hsic = HSIC(X, Y)

    assert len(hsic) == X.shape[1]
    assert all(hsic >= 0)

    x = np.random.rand(10, 1)
    assert np.all(HSIC(x, x**2) > hsic)


def test_mmd():
    mmd = MMD(X, Y)

    assert len(mmd) == X.shape[1]
    assert all(mmd >= 0)

    x = np.random.rand(10, 1)
    assert np.all(MMD(x, x**2) > mmd)
