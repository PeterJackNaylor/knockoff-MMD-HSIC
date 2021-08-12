import numpy as np

from knock_off.association_measures.hsic import HSIC
from knock_off.association_measures.mmd import MMD

X = np.random.normal(size=(10, 50))
Y = np.random.normal(size=10)


def test_hsic():
    hsic = HSIC(X, Y)

    assert len(hsic) == X.shape[1]


def test_mmd():
    mmd = MMD(X, Y)

    assert len(mmd) == X.shape[1]
