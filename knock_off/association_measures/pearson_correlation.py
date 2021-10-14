import numpy as np
from scipy.stats import pearsonr

def pearson_correlation(X, Y):
    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1
    pearson_stats = np.zeros((d, 1))
    for i in range(d):
        try:
            pearson_stats[i] = np.array([np.float32(abs(pearsonr(X[:, i], Y[:, 0])[0]))])
        except:
            pearson_stats[i] = float('nan')

    return pearson_stats
