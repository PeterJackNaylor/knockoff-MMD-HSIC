from .kernel_tools import get_kernel_function


def MMD(X, Y, kernel='gaussian'):

    n, d = X.shape
    ny = len(Y)

    assert n == ny

    kernel, kernel_params = get_kernel_function(kernel, nfeats=d)

    Ky = kernel(Y, **kernel_params)
    mmd_stats = []

    for x in X.T:
        Kx = kernel(x, **kernel_params)
        Kxy = kernel(x, Y, **kernel_params)

        # set diagonal to 0?
        mmd = (Kx + Ky - 2*Kxy).sum() / (n*(n-1))
        mmd_stats.append(mmd)

    return mmd_stats
