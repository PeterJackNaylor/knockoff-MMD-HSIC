import numpy as np
from simulations_X import options, produce_synthetic_data


def formula(x, n=None):
    if n is None:
        n = x.shape[0]

    eps = np.random.normal(loc=0.0, scale=1.0, size=n)
    y_star = x[:, 0:10].sum(axis=1) + 10 ** 0.5 + eps

    def f(x):
        if x < 0:
            y = 0
        elif x < 2:
            y = 1
        elif x < 4:
            y = 2
        elif x < 6:
            y = 3
        elif x < 8:
            y = 4
        else:
            y = 5
        return y

    y = np.vectorize(f)(y_star)

    return y


def main():
    opt = options()
    produce_synthetic_data(opt.n, opt.p, formula, correlated=True)


if __name__ == "__main__":
    main()
