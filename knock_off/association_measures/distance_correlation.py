
# from dcor import distance_correlation as dc
import numpy as np
import dcor

def distance_corr(X, Y):
    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1
    dc_stats = np.zeros((d, 1))

    for i in range(d):
        dc_stats[i] = dcor.distance_correlation(X[:, i], Y[:, 0])

    return dc_stats
