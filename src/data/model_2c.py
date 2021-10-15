import numpy as np
from simulations_X import options, produce_synthetic_data


def formula(x, n=None):
    if n is None:
        n = x.shape[0]

    lam = np.exp(x[:, 0:10].sum(axis=1))
    y = np.random.poisson(lam=lam, size=n).astype(float)

    return y


def main():
    opt = options()
    produce_synthetic_data(opt.n, opt.p, formula)


if __name__ == "__main__":
    main()
