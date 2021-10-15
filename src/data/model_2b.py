import numpy as np
from simulations_X import options, produce_synthetic_data


def formula(x, n=None):
    if n is None:
        n = x.shape[0]

    x1 = x[:, 0]
    x2 = x[:, 1]
    x3 = x[:, 2]
    x4 = x[:, 3]

    x1 = 3 * x1
    x2 = 3 * x2 ** 3
    x3 = 3 * x3 ** -1
    x4 = 5 * (x4 > 0).astype(int)

    eps = np.random.normal(loc=0.0, scale=1.0, size=n)

    y = x1 + x2 + x3 + x4 + eps
    return y


def main():
    opt = options()
    produce_synthetic_data(opt.n, opt.p, formula)


if __name__ == "__main__":
    main()
