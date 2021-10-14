import numpy as np
from scipy.stats import kendalltau, spearmanr


def tr(X, Y):
    n, d = X.shape
    ny, nd = Y.shape

    assert n == ny
    assert nd == 1

    tr_stats = np.zeros((d, 1))

    for i in range(d):
        tau = kendalltau(X[:, i], Y[:, 0]).correlation
        rho = spearmanr(X[:, i], b=Y[:, 0]).correlation
        tr_stats[i] = abs(3 * tau  - 2 * rho)

    return  tr_stats

if __name__ == "__main__":
    x, y = [1,2,3,4,5], [5,6,7,8,7]
    print("rho: ", spearmanr(x, y).correlation)
    print("tau: ", kendalltau(x, y).correlation)
    print(f"{tr(x,y)=}")
