"""
Implementation of algorithm 1 of paper Model-Free Feature Screening and FDR Control with Knockoff Features
with any type of metrics

"""

import numpy as np

from abc import ABC, abstractmethod
import numpy.typing as npt
from sklearn.base import BaseEstimator

from utils import screen, build_knockoff
from association_measures import projection_corr

class KnockOff(BaseEstimator, ABC):

    _required_parameters = ["", "lambda_1", "lambda_2", "loss", "regul", "pos"]

    def __init__(
        self,
        alpha: float = 1.0,
        n1: int = 50,
        d: int = 20,
        measure_stat: str = "PC"

        ) -> None:
        super().__init__()
        self.alpha = alpha
        self.n1 = n1
        self.d = d
        assert measure_stat in ["PC", "HSIC", "MMD"]
        self.measure_stat = measure_stat
        if self.measure_stat == "PC":
            self.tr = projection_corr


    def fit(self, X: npt.ArrayLike, y: npt.ArrayLike) -> KnockOff:
        n = X.shape[0]
        n2 = n - self.n1
        ## need to check
        assert self.d < n2 / 2

        # split data
        indices = np.arange(n)
        np.random.shuffle(indices)
        set_one = indices[:self.n1]
        set_two = indices[self.n1:]

        X1, y1 = X[set_one, :], y[set_one]
        X2, y2 = X[set_two, :], y[set_two]

        ## screening process
        A_d_hat = screen(X1, y1, self.measure)

        ## knock off step
        # construct knock off variables
        wjs = build_knockoff(X2[:, A_d_hat], y2)
        import pdb; pdb.set_trace()

